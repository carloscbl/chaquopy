from __future__ import absolute_import, division, print_function

from unittest import TestCase

from java import *

from com.chaquo.python import TestStaticProxy as TSP
import static_proxy.basic as basic


class TestStaticProxy(TestCase):

    def test_basic(self):
        BA = basic.BasicAdder
        TSP.ba1, TSP.ba2 = BA(1), BA(2)
        self.assertEqual(5, TSP.ba1.add(4))
        self.assertEqual(6, TSP.ba2.add(4))

    # Could happen if static proxies aren't regenerated correctly.
    def test_wrong_load_order(self):
        with self.assertRaisesRegexp(TypeError, "static_proxy class "
                                     "com.chaquo.python.static_proxy.WrongLoadOrder loaded "
                                     "before its Python counterpart"):
            from com.chaquo.python.static_proxy import WrongLoadOrder

    # Could happen if static proxies aren't regenerated correctly.
    def test_wrong_bases(self):
        with self.assertRaisesRegexp(TypeError, "expected extends java.lang.Object, but Java "
                                     "class actually extends java.lang.Exception"):
            class WrongExtends(static_proxy(package="com.chaquo.python.static_proxy")):
                pass

        with self.assertRaisesRegexp(TypeError, r"expected implements \['java.lang.Runnable', "
                                     r"'com.chaquo.python.StaticProxy'], but Java class actually "
                                     r"implements \[]"):
            from java.lang import Runnable
            class WrongImplements(static_proxy(None, Runnable,
                                               package="com.chaquo.python.static_proxy")):
                pass

    def test_gc(self):
        from pyobjecttest import DelTrigger as DT

        DT.reset()
        gc = basic.GC()
        DT.assertTriggered(self, False)
        TSP.o1 = gc
        del gc
        DT.assertTriggered(self, False)
        TSP.o1 = None
        DT.assertTriggered(self, True)

        DT.reset()
        TSP.o1 = basic.GC()
        DT.assertTriggered(self, False)
        gc = TSP.o1
        TSP.o1 = None
        DT.assertTriggered(self, False)
        del gc
        DT.assertTriggered(self, True)