#!/usr/bin/python3
""" A module containing a class entry point fod a Command Line Interpreter """

import json
import os
import cmd
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.review import Review
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity

# A list containing all claseess
CLASS_LIST = [
        "BaseModel", "User", "State", "City", "Amenity", "Place", "Review"
        ]

# All functions list
FUNCTIONS = ["all", "count", "show", "destroy", "update"]


class HBNBCommand(cmd.Cmd):
    """ Serves as the console's entry point """
    prompt = "(hbnb) "

    def do_quit(self, line):
        """
        Used to exit the program
        Args:
            line: holds the command line argumentss.
        """
        return (True)

    def do_EOF(self, line):
        """
        Used to Exit the program
           Args:
               line: holds command line arguments.
        """
        print()
        return (True)

    def emptyline(self):
        """
        Handles no command given
        """
        pass

    def do_create(self, args):
        """
        Creates Instances of BsseModel
        """
        arg_list1 = args.split()
        if len(arg_list1) < 1:
            print("** class name missing **")
            return (False)

        arg = arg_list1[0]

        if arg not in CLASS_LIST:
            print("** class doesn't exist **")
            return (False)
        obj = self.create_obj(arg)
        if obj:
            print(obj)

    def create_obj(self, class_name):
        """ Creates object """
        if class_name == "BaseModel":
            base_model = BaseModel()
            base_model.save()
            return (base_model.id)
        if class_name == "User":
            user = User()
            user.save()
            return (user.id)
        if class_name == "State":
            state = State()
            state.save()
            return (state.id)
        if class_name == "City":
            city = City()
            city.save()
            return (city.id)
        if class_name == "Amenity":
            amenity = Amenity()
            amenity.save()
            return (amenity.id)
        if class_name == "Place":
            place = Place()
            place.save()
            return (place.id)
        if class_name == "Review":
            review = Review()
            review.save()
            return (review.id)
        return (False)

    def do_all(self, arg):
        """
        Used to print tring representations of all instances whether based
        or the classor not.
        Args:
            arg: Holds command line arguments.
        """
        arg_list = arg.split()
        object_dict = storage.all()
        if not arg_list:
            object_list = list(object_dict.values())
        elif arg_list[0] not in CLASS_LIST:
            print("** class doesn't exist **")
            return
        else:
            object_list = [
                    i for i in object_dict.values()
                    if i.__class__.__name__ == arg_list[0]
                    ]
            print([str(i) for i in object_list])

    def do_show(self, args):
        """
        Used to print the string representation of an instance based on class
        name.
           Args:
               args: Holds  command line arguments.
        """
        args_list = args.split()
        if len(args_list) < 1:
            print("** class name missing **")
            return (False)
        elif args_list[0] not in CLASS_LIST:
            print("** class doesn't exist **")
            return (False)
        elif len(args_list) < 2:
            print("** instance id missing **")
            return (False)
        else:
            i = args_list[1]
            key = "{}.{}".format(args_list[0], i)
            object_dict = storage.all()
            if key in object_dict:
                print(object_dict[key])
            else:
                print("** no instance found **")

    def do_destroy(self, args):
        """
        Used to delete an instance based on class name & id
           Args:
               args: Holds command line arguments
        """
        args_list = args.split()
        if len(args_list) < 1:
            print("** class name missing **")
            return (False)
        elif args_list[0] not in CLASS_LIST:
            print("** class doesn't exist **")
            return (False)
        elif len(args_list) < 2:
            print("** instance id missing **")
            return (False)
        else:
            i = args_list[1]
            key = "{}.{}".format(args_list[0], i)
            object_dict = storage.all()
            if key in object_dict:
                del object_dict[key]
            else:
                print("** no instance found **")
            storage.save()

    def do_update(self, args):
        """
        Used to update instance through adding/ updating attributey
           Args:
               args: Holds command line arguments.
        """
        attrs = {}
        if "from_func" in args:
            try:
                arg = args.split()
                attrs = json.loads(arg[2])
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e}")
                return (False)
        else:
            arg = args.split()

        if len(arg) < 1:
            print("** class name missing **")
            return (False)
        if arg[0] not in CLASS_LIST:
            print("** class doesn't exist **")
            return (False)
        if len(arg) < 2:
            print("** instance id missing **")
            return (False)
        i = arg[1]
        key = "{}.{}".format(arg[0], i)
        object_dict = storage.all()

        if key not in object_dict:
            print("** no instance found **")
            return (False)
        elif len(arg) < 3:
            print("** attribute name missing **")
            return (False)
        elif len(arg) < 4:
            print("** value missing **")
            return (False)
        else:
            j = object_dict[key]
            if len(attrs) > 0:
                for key, val in attrs.items():
                    setattr(j, key, val)
            else:
                attribute_name = arg[2]
                attribute_value = arg[3].strip("\"")
                setattr(j, attribute_name, attribute_value)
                j.save()

    def __do_count(self, obj):
        """
        Used to count number of objects in the storage system
        """
        cnt = 0  # Initialize count
        object_dict = storage.all()

        for key, value in object_dict.items():
            dictionary2 = value.to_dict()
            if dictionary2["__class__"] == obj:
                cnt += 1  # Increment

        return (cnt)  # return count

    def _default_process(self, line):
        """
        Used to handle the execution of default method
            Args:
                line: Holds commandline arguments
        """
        args = line.split(".", 1)
        if len(args) != 2:
            return (cmd.Cmd.default(self, line))
        if args[0] not in CLASS_LIST:
            return (cmd.Cmd.default(self, line))
        if "(" not in args[1] or ")" not in args[1]:
            return (cmd.Cmd.default(self, line))
        args = line.replace("(", " ").replace(")", " ")
        args = args.replace('"', '').replace("'", " ").replace(",", "")
        args = args.strip()
        if not self.execute_command(line, args):
            cmd.Cmd.default(self, line)

    def default(self, line):
        """ Handles where no commands matches ones on the list """
        return self._default_process(line)

    def execute_command(self, line, args):
        """
        This calls all methods to execute
            Args:
                line: Holds command line arguments
                args: an array that contains arguments
            Return:
                  True when successfully run and False when a function failse
        """
        args_list = args.split(" ")
        class_name = args_list[0].split(".")[0]
        function_name = args_list[0].split(".")[1]
        length = len(args_list)
        if function_name not in FUNCTIONS:
            return (False)
        del args_list[0]
        args_list.insert(0, class_name)

        if function_name == "all":
            self.do_all(class_name)
            return (True)
        if function_name == "count":
            self.__do_count(class_name)
            return (True)
        if function_name == "show":
            self.do_show(" ".join([args_list[x] for x in range(length)]))
            return (True)
        if function_name == "destroy":
            self.do_destroy(" ".join([args_list[x] for x in range(length)]))
            return (True)

        new_args_list = line.split(" ", 1)
        to_data = ""

        if len(new_args_list) > 1:
            try:
                new_args_list[1] = new_args_list[1].replace("'", '"')
                to_data = json.loads(new_args_list[1].strip(")"))
            except Exception as ie:
                to_data = ""

        if function_name == "update" and isinstance(to_data, dict):
            arr = [class_name, args_list[1], json.dumps(to_data)]
            arr.append("from_func")
            self.do_update(arr)
            return (True)
        else:
            if length > 4:
                length = 4
                arr = [args_list[x].strip(")") for x in range(length)]
                self.do_update(" ".join(arr))
                return (True)
            return (False)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
