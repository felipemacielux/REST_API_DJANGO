# Test Coverage -> métrica da Engenharia de Software para saber quanto um método está coberto de testes 
import unittest
def dividir(a, b): 
    if b == 0:
        return None
    return a /b

class TestDividir(unittest.TestCase):
    def test_divisao_por_1_retorna_o_proprio_numero(self):
        self.assertEqual(dividir(10,1), 10)

    def test_divisao_por_0_retorna_none(self):
        self.assertEqual(dividir(10,0), None)


if __name__ == '__main__':
    unittest.main()