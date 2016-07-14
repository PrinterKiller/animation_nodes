from unittest import TestCase
from . base_lists import IntegerList

class TestInsertion(TestCase):
    def testAtStart(self):
        a = IntegerList.fromValues((0, 1, 2, 3))
        a.insert(0, 10)
        self.assertEqual(a, (10, 0, 1, 2, 3))

    def testAtEnd(self):
        a = IntegerList.fromValues((0, 1, 2, 3))
        a.insert(4, 10)
        self.assertEqual(a, (0, 1, 2, 3, 10))

    def testAfterEnd(self):
        a = IntegerList.fromValues((0, 1, 2, 3))
        a.insert(50, 10)
        self.assertEqual(a, (0, 1, 2, 3, 10))

    def testInMiddle(self):
        a = IntegerList.fromValues((0, 1, 2, 3))
        a.insert(2, 10)
        self.assertEqual(a, (0, 1, 10, 2, 3))

    def testLengthUpdate(self):
        a = IntegerList.fromValues((0, 1, 2, 3))
        a.insert(2, 1)
        self.assertEqual(len(a), 5)

    def testNegativeIndex(self):
        a = IntegerList.fromValues((0, 1, 2, 3))
        a.insert(-1, 10)
        self.assertEqual(a, (0, 1, 2, 10, 3))
        a.insert(-3, 20)
        self.assertEqual(a, (0, 1, 20, 2, 10, 3))
        a.insert(-100, 30)
        self.assertEqual(a, (30, 0, 1, 20, 2, 10, 3))

class TestRichComparison(TestCase):
    def testEqual_Left(self):
        a = IntegerList.fromValues((0, 1, 2, 3))
        self.assertTrue(a == (0, 1, 2, 3))
        self.assertTrue(a == [0, 1, 2, 3])
        self.assertFalse(a == [0, 1, 2, 3, 4])
        self.assertFalse(a == (0, 1, 2, 3, 4))

    def testEqual_Right(self):
        a = IntegerList.fromValues((0, 1, 2, 3))
        self.assertTrue((0, 1, 2, 3) == a)
        self.assertTrue([0, 1, 2, 3] == a)
        self.assertFalse([0, 1, 2, 3, 4] == a)
        self.assertFalse((0, 1, 2, 3, 4) == a)

    def testEqual_Both(self):
        a = IntegerList.fromValues((0, 1, 2, 3))
        b = IntegerList.fromValues((0, 1, 2, 3))
        c = IntegerList.fromValues((0, 1, 2, 3, 4))
        d = IntegerList.fromValues((0, 1, 2, 4))
        self.assertTrue(a == b)
        self.assertFalse(a == c)
        self.assertFalse(a == d)

class TestClear(TestCase):
    def testLengthAfterClear(self):
        a = IntegerList.fromValues((0, 1, 2, 3))
        self.assertEqual(len(a), 4)
        a.clear()
        self.assertEqual(len(a), 0)

class TestCopy(TestCase):
    def testDifferentMemoryAdresses(self):
        a = IntegerList()
        b = a.copy()
        self.assertNotEqual(id(a), id(b))

    def testIndependency(self):
        a = IntegerList()
        b = a.copy()
        a.append(5)
        self.assertEqual(len(a), 1)
        self.assertEqual(len(b), 0)

class TestAppend(TestCase):
    def testEmptyList(self):
        a = IntegerList()
        a.append(5)
        self.assertEqual(a, [5])

    def testLength(self):
        a = IntegerList.fromValues((1, 2, 3, 4))
        a.append(5)
        self.assertEqual(len(a), 5)

    def testNormal(self):
        a = IntegerList.fromValues((1, 2, 3))
        a.append(4)
        self.assertEqual(a, [1, 2, 3, 4])

    def testMany(self):
        a = IntegerList()
        for i in range(10):
            a.append(i)
        self.assertEqual(a, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])