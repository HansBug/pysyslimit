pysyslimit.models.permission
======================================

.. py:currentmodule:: pysyslimit.models.permission

FileSinglePermission
-------------------------

.. autoclass:: FileSinglePermission
    :members: __init__, readable, writable, executable, value, __int__, sign, __eq__, __hash__, __str__, __repr__, load_by_value, load_by_sign, loads, __add__, __radd__, __iadd__, __or__, __ror__, __ior__, __and__, __rand__, __iand__, __sub__, __rsub__, __isub__


FileUserPermission
--------------------------

.. autoclass:: FileUserPermission


FileGroupPermission
--------------------------

.. autoclass:: FileGroupPermission


FileOtherPermission
--------------------------

.. autoclass:: FileOtherPermission


FilePermission
---------------------------

.. autoclass:: FilePermission
    :members: __init__, user, group, other, oct_value, value, __int__, sign, __eq__, __hash__, __str__, __repr__, load_by_value, load_by_oct_value, load_by_sign, loads, load_from_file, __add__, __radd__, __iadd__, __or__, __ror__, __ior__, __and__, __rand__, __iand__, __sub__, __rsub__, __isub__
