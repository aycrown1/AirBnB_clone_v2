#!/usr/bin/python3
import unittest
import inspect
import pep8
import console
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO

class TestHBNBCommand(unittest.TestCase):

    def setUp(self):
        self.cmd = HBNBCommand()

    def test_create(self):
        """Test the 'create' command functionality"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cmd.onecmd("create BaseModel")
            output = mock_stdout.getvalue()
            self.assertTrue(isinstance(output, str))

    def test_show(self):
        """Test the 'show' command functionality"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cmd.onecmd("create BaseModel")
            self.cmd.onecmd("show BaseModel")
            output = mock_stdout.getvalue()
        self.assertTrue("** instance id missing **" in output)

    def test_destroy(self):
        """Test the 'destroy' command functionality"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cmd.onecmd("create BaseModel")
            self.cmd.onecmd("destroy BaseModel")
            output = mock_stdout.getvalue()
        self.assertTrue("BaseModel" not in output)

    def test_all(self):
        """Test the 'all' command functionality"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cmd.onecmd("create BaseModel")
            self.cmd.onecmd("create User")
            self.cmd.onecmd("all")
            output = mock_stdout.getvalue()
        self.assertIn("[BaseModel]", output)
        self.assertIn("[User]", output)

        with patch('sys.stdout', new=StringIO()) as f:
            self.cmd.onecmd("all State")
            self.assertEqual("[]\n", f.getvalue())

    def test_update(self):
        """Test the 'update' command functionality"""
        
        with patch('sys.stdout', new=StringIO()) as f:
            self.cmd.onecmd("update")
            self.assertEqual("** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.cmd.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())


    def test_pep8_console(self):
        """Pep8 console.py"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["console.py"])
        self.assertEqual(p.total_errors, 0, 'fix Pep8')

    def test_docstrings_in_console(self):
        """checking for docstrings"""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)



if __name__ == '__main__':
    unittest.main()
