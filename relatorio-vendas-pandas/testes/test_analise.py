import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from analise import carregar_vendas, gerar_relatorios, reais, salvar_relatorios


class TesteAnalise(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.caminho = Path(self.pasta.name) / "exemplo.csv"
        self.caminho.write_text(
            "data,produto,categoria,quantidade,preco_unitario,regiao\n"
            "2026-01-03,Caneta,Papelaria,2,5.00,São Paulo\n"
            "2026-01-05,Caderno,Papelaria,1,30.00,São Paulo\n"
            "2026-02-01,Caneta,Papelaria,3,5.00,Campinas\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.pasta.cleanup()

    def test_faturamento_total(self):
        vendas = carregar_vendas(self.caminho)
        self.assertAlmostEqual(vendas["valor_total"].sum(), 55.0)
        self.assertEqual(int(vendas["quantidade"].sum()), 6)

    def test_tabelas(self):
        relatorios = gerar_relatorios(carregar_vendas(self.caminho))
        self.assertEqual(len(relatorios["meses"]), 2)
        self.assertAlmostEqual(relatorios["produtos"].iloc[0]["faturamento"], 30.0)

    def test_exportacao_csv(self):
        relatorios = gerar_relatorios(carregar_vendas(self.caminho))
        destino = Path(self.pasta.name) / "saida"
        salvar_relatorios(relatorios, destino)
        self.assertTrue((destino / "relatorio_categorias.csv").exists())
        self.assertEqual(len(pd.read_csv(destino / "relatorio_produtos.csv")), 2)

    def test_rejeita_quantidade_negativa(self):
        texto = self.caminho.read_text(encoding="utf-8").replace(",2,5.00,", ",-2,5.00,")
        self.caminho.write_text(texto, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "maiores que zero"):
            carregar_vendas(self.caminho)

    def test_rejeita_coluna_faltando(self):
        self.caminho.write_text("data,produto\n2026-01-01,Caneta\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Colunas ausentes"):
            carregar_vendas(self.caminho)

    def test_formatacao_moeda(self):
        self.assertEqual(reais(1245.3), "R$ 1.245,30")


if __name__ == "__main__":
    unittest.main()
