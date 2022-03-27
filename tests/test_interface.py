import unittest
import os

from dbinterpy.interface import DatabaseInterface


class TestInterface(unittest.TestCase):
    def test_create_connect(self):
        """
        Test that the database is created with valid headings
        """
        headings = {'name': 'TEXT', 'age': 'INT'}
        interf_create = DatabaseInterface('people.db', headings)
        x = os.system("ls people.db")
        self.assertEqual(x, 0)
        del(interf_create)
        interf_conn = DatabaseInterface('people.db')
        self.assertEqual(headings, interf_conn.keys_types)
        os.system("rm people.db")

    def test_add(self):
        """
        Test that elements are added to the database properly
        """
        headings = {'name': 'TEXT', 'age': 'INT'}
        interf = DatabaseInterface('people.db', headings)
        interf.add_one({'name': 'Steve', 'age': 25})
        interf.add_many([{'name': 'Emma', 'age': 22},
                         {'name': 'Alan', 'age': 35}])

        check = [(1, 'Steve', 25), (2, 'Emma', 22), (3, 'Alan', 35)]

        self.assertEqual(interf.lookup(), check)
        os.system("rm people.db")

    def test_lookup_delete(self):
        """
        Test that looking up and deleting is implemented correctly
        """
        headings = {'name': 'TEXT', 'age': 'INT'}
        interf = DatabaseInterface('people.db', headings)
        interf.add_one({'name': 'Steve', 'age': 25})
        interf.add_many([{'name': 'Emma', 'age': 22},
                         {'name': 'Alan', 'age': 35}])

        check = [(1, 'Steve', 25), (2, 'Emma', 22)]
        interf.delete(3)
        self.assertEqual(interf.lookup(), check)
        self.assertRaises(TypeError, interf.lookup, 'age') 
        self.assertRaises(TypeError, interf.lookup,
                          [('age', 22), ['name', 'Gloria', 6]])

        interf.add_one({'name': 'Anna', 'age': 25})
        check = [(1, 'Steve', 25), (3, 'Anna', 25)]
        self.assertEqual(interf.lookup(('age', 25)), check)

        check = [(1, 'Steve', 25)]
        self.assertEqual(interf.lookup([('age', 25),
                         ('name', 'Steve')]), check)

        check = [(1, 'Steve', 25)]
        self.assertEqual(interf.lookup(('name', 'Steve')), check)

        os.system("rm people.db")

    def test_update(self):
        """
        Test updating the database and executing custom SQL commands.
        """
        headings = {'name': 'TEXT', 'age': 'INT'}
        interf = DatabaseInterface('people.db', headings)
        interf.add_one({'name': 'Steve', 'age': 25})
        interf.add_one({'name': 'Charlie', 'age': 22})

        interf.update(2, 'name', 'Charles')
        check = [(2, 'Charles', 22)]
        self.assertEqual(interf.lookup(('name', 'Charles')), check)

        interf.update(1, 'age', 23)
        check = [(1, 'Steve', 23)]
        self.assertEqual(interf.lookup(('name', 'Steve')), check)

        interf.execute("UPDATE people SET 'name' = 'Charley' WHERE rowid = 2")
        interf.execute("UPDATE people SET 'age' = 24 WHERE rowid = 2")
        check = [(2, 'Charley', 24)]
        self.assertEqual(interf.lookup(('name', 'Charley')), check)

        self.assertRaises(TypeError, interf.execute, 24)
        self.assertTrue(isinstance(repr(interf), str))
        self.assertTrue(isinstance(str(interf), str))

        os.system("rm people.db")


if __name__ == '__main__':
    unittest.main(verbosity=2)

