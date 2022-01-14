pysyslimit.models.user
==============================

.. py:currentmodule:: pysyslimit.models.user

SystemUser
------------------

.. autoclass:: SystemUser
    :members: __init__, name, passwd, uid, gid, gecos, dir, shell, primary_group, groups, apply, __eq__, __hash__, __str__, __repr__, current, root, nobody, all, load_from_file, loads


SystemGroup
------------------

.. autoclass:: SystemGroup
    :members: __init__, name, passwd, gid, mem, apply, __eq__, __hash__, __str__, __repr__, users, members, full_members, current, current_attaches, nogroup, root, load_from_file, loads


SystemGroupAttaches
---------------------------

.. autoclass:: SystemGroupAttaches
    :members: groups, append, clear, reset
