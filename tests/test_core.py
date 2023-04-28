
import os
import sys

# adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.process.src.faker.faker_data import FakerCreator
from services.process.src.spark_manipulator.main import SparkManipulator
import unittest
from datetime import datetime
from unittest.mock import patch


############################################################ Testes do fake creator ########################################################################
class TestFakerCreator(unittest.TestCase):

    def setUp(self):
        self.faker_creator = FakerCreator(3,TEST=True)

    def test_create_fake_data_associado(self):
        self.faker_creator.create_fake_data_associado()
        self.assertEqual(len(self.faker_creator.associado), 3)
        self.assertTrue(isinstance(self.faker_creator.associado[0]['nome'], str))
        self.assertTrue(isinstance(self.faker_creator.associado[0]['sobrenome'], str))
        self.assertTrue(isinstance(self.faker_creator.associado[0]['idade'], int))
        self.assertTrue(isinstance(self.faker_creator.associado[0]['email'], str))

    def test_create_fake_data_conta(self):
        self.faker_creator.create_fake_data_associado()
        self.faker_creator.create_fake_data_conta()
        self.assertEqual(len(self.faker_creator.conta), 3)
        self.assertTrue(isinstance(self.faker_creator.conta[0]['tipo'], str))
        self.assertTrue(isinstance(self.faker_creator.conta[0]['data_criacao'], datetime))
        self.assertTrue(isinstance(self.faker_creator.conta[0]['id_associado'], int))

    def test_create_fake_data_cartao(self):
        self.faker_creator.create_fake_data_associado()
        self.faker_creator.create_fake_data_conta()
        self.faker_creator.create_fake_data_cartao()
        self.assertEqual(len(self.faker_creator.cartao), 3)
        self.assertTrue(isinstance(self.faker_creator.cartao[0]['num_cartao'], str))
        self.assertTrue(isinstance(self.faker_creator.cartao[0]['nom_impresso'], str))
        self.assertTrue(isinstance(self.faker_creator.cartao[0]['id_conta'], int))
        self.assertTrue(isinstance(self.faker_creator.cartao[0]['id_associado'], int))

    def test_create_fake_data_movimentacao(self):
        self.faker_creator.create_fake_data_associado()
        self.faker_creator.create_fake_data_conta()
        self.faker_creator.create_fake_data_cartao()
        self.faker_creator.create_fake_data_movimentacao()
        self.assertEqual(len(self.faker_creator.movimentacao), 300)
        self.assertTrue(isinstance(self.faker_creator.movimentacao[0]['vlr_transacao'], float))
        self.assertTrue(isinstance(self.faker_creator.movimentacao[0]['data_movimento'], datetime))
        self.assertTrue(isinstance(self.faker_creator.movimentacao[0]['id_cartao'], int))


############################################################ Testes do spark manipulator #######################################################################
class TestSparkManipulator(unittest.TestCase):
    def setUp(self):
        self.spark_manipulator = SparkManipulator()

    def test_rename_columns(self):
        # create test dataframe
        df = self.spark_manipulator.spark.createDataFrame([(1, "foo"), (2, "bar")], ["id", "name"])
        self.spark_manipulator.data["table_name"] = df

        self.spark_manipulator.rename_columns("table_name", "name", "new_name")
        self.assertTrue("new_name" in self.spark_manipulator.data["table_name"].columns)

    def test_join_tables(self):
        # create test dataframes
        df1 = self.spark_manipulator.spark.createDataFrame([(1, "foo"), (2, "bar")], ["id", "name"])
        df2 = self.spark_manipulator.spark.createDataFrame([(1, "foo"), (2, "baz")], ["id", "value"])
        self.spark_manipulator.data["table1"] = df1
        self.spark_manipulator.data["table2"] = df2

        self.spark_manipulator.join_tables("table1", "table2", "id", "inner")
        self.assertTrue("join" in self.spark_manipulator.data)

    def test_select_columns(self):
        # create test dataframe
        df = self.spark_manipulator.spark.createDataFrame([(1, "foo"), (2, "bar")], ["id", "name"])
        self.spark_manipulator.data["table_name"] = df

        self.spark_manipulator.select_columns("table_name", ["id"])
        self.assertEqual(len(self.spark_manipulator.data["table_name_selected"].columns), 1)


if __name__ == '__main__':
    unittest.main()