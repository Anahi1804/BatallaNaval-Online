# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.1

from __future__ import annotations
import IcePy

from Juego.Fila import _Juego_Fila_t

_Juego_Matriz_t = IcePy.defineSequence("::Juego::Matriz", (), _Juego_Fila_t)

__all__ = ["_Juego_Matriz_t"]
