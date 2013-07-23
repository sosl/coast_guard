import operator

class BaseConfigType(object):
    """The base class of ConfigType objects.

        ConfigType objects are used to define the parameters
        of cleaner config-strings.
    """
    name = NotImplemented
    description = None

    def __init__(self):
        pass

    def get_param_value(self, paramstr):
        """Parse a parameter string.

            Inputs:
                paramstr: The parameter string to parse.

            Output:
                newval: The new parameter value.
        """
        raise NotImplementedError("The method _get_param_value(...) of " \
                                    "ConfigType objects must be implemented " \
                                    "by its subclases.")

    def normalize_param_string(self, paramstr):
        """Return a normalized version of the parameter string.

            Inputs:
                paramstr: The parameter string to parse.

            Output:
                normed: The normalized parameter string.
        """
        return paramstr
    
    def get_help(self):
        helpstr = "Type: %s" % self.name.strip()
        if self.description is not None:
            helpstr += " - %s" % self.description.strip()
        return helpstr


class FloatVal(BaseConfigType):
    """A configuration type for floating-point values.
    """
    name = "float"

    def get_param_value(self, paramstr):
        """Parse 'paramstr' as a normal floating-point value.
            The previous parameter value is ignored.
        """
        return float(paramstr)


class BoolVal(BaseConfigType):
    """A configuration type for boolean values.
    """
    name = "bool"
    description = "The following values are recognised (case insensitive): " \
                    "true, 1, y, yes, false, 0, n, no"

    def get_param_value(self, paramstr):
        """Parse 'paramstr' as a boolean value. The following values 
            are recognised (case insensitive):
                true, 1, y, yes, false, 0, n, no
            The previous parameter value is ignored.
        """
        paramstr = paramstr.lower()
        if paramstr in ('true', '1', 'y', 'yes'):
            boolval = True
        elif paramstr in ('false', '0', 'n', 'no'):
            boolval = False
        else:
            raise ValueError("The parameter string '%s' is not recognized. " \
                                "Only the following (case-insensitive) " \
                                "values are allowed: true, 1, y, yes, " \
                                "false, 0, n, no" % paramstr)
        return boolval

    def normalize_param_string(self, paramstr):
        """Return a normalized version of the parameter string.
        """
        return str(self.get_param_value(paramstr))


def _str_to_intlist(paramstr):
    """Parse 'paramstr' as a list of integes. The format must
        be <int>[;<int>>...]. 
    """
    if paramstr.strip():
        # Contains at least one element
        intstrs = paramstr.split(';')
        return [int(ss) for ss in intstrs]
    else:
        return []


class IntList(BaseConfigType):
    """A configuration type for a list of integers.
    """
    name = "list of integers, or None"
    description = "an integer list <int>[;<int>...], or None."
    
    def get_param_value(self, paramstr):
        if paramstr.lower() == "none":
            return None
        else:
            return _str_to_intlist(paramstr)

    def normalize_param_string(self, paramstr):
        """Return a normalized version of the parameter string.
        """
        val = self.get_param_value(paramstr)
        if val is None:
            return "None"
        else:
            ints = val
            return ";".join(["%d" % ii for ii in ints])


class IntListList(BaseConfigType):
    """A configuration type for a list of integer lists.
    """
    name = "list of integer lists, or None"
    description = "an integer list <int>[;<int>...][;;<int>[;<int>...]...], or None."
    
    def get_param_value(self, paramstr):
        """Parse 'paramstr' as a list of integer lists. The format must
            be <int>[;<int>...][;;<int>[;<int>...]...]. 
        """
        if paramstr.lower() == "none":
            return None
        intlists = []
        if paramstr.strip():
            remainder = paramstr
            while remainder:
                liststr, sep, remainder = remainder.partition(';;')
                intlists.append(_str_to_intlist(liststr))
        return intlists
    
    def normalize_param_string(self, paramstr):
        """Return a normalized version of the parameter string.
        """
        val = self.get_param_value(paramstr)
        if val is None:
            return "None"
        else:
            intlists = val
            intliststrs = []
            for ints in intlists:
                intliststrs.append(";".join(["%d" % ii for ii in ints]))
            return ";;".join(intliststrs)


class IntPairList(BaseConfigType):
    """A configuration type for a list of integer pairs.
    """
    name = "list of integer pairs"
    description = "a list of integer pairs <int>:<int>[;<int>:<int>...]. " \

    def _to_int_pair(self, paramstr):
        intstrs = paramstr.split(':')
        if len(intstrs) != 2:
            raise ValueError("Bad number of integer strings in '%s'. Each " \
                             "integer should be separated by ':'." % paramstr)
        return (int(intstrs[0]), int(intstrs[1]))

    def get_param_value(self, paramstr):
        """Parse 'paramstr' as a list of integer pairs. The format must
            be <int>:<int>[;<int>:<int>...]. 
        """
        if paramstr.strip():
            # Contains at least one pair
            pairstrs = paramstr.split(';')
            return [self._to_int_pair(ss) for ss in pairstrs]
        else:
            return []
    
    def normalize_param_string(self, paramstr):
        """Return a normalized version of the parameter string.
        """
        pairs = self.get_param_value(paramstr)
        return ";".join(["%d:%d" % pair for pair in pairs])
