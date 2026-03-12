# Copyright (c) ZeroC, Inc.

# slice2py version 3.8.1

from __future__ import annotations
import IcePy

from Ice.Object import Object

from Ice.ObjectPrx import ObjectPrx
from Ice.ObjectPrx import checkedCast
from Ice.ObjectPrx import checkedCastAsync
from Ice.ObjectPrx import uncheckedCast

from Ice.OperationMode import OperationMode

from Juego.Matriz import _Juego_Matriz_t

from Juego.MotorMultijugador_forward import _Juego_MotorMultijugadorPrx_t

from abc import ABC
from abc import abstractmethod

from typing import TYPE_CHECKING
from typing import overload

if TYPE_CHECKING:
    from Ice.Current import Current
    from collections.abc import Awaitable
    from collections.abc import Sequence


class MotorMultijugadorPrx(ObjectPrx):
    """
    Notes
    -----
        The Slice compiler generated this proxy class from Slice interface ``::Juego::MotorMultijugador``.
    """

    def registrarJugador(self, totalEsperados: int, context: dict[str, str] | None = None) -> int:
        return MotorMultijugador._op_registrarJugador.invoke(self, ((totalEsperados, ), context))

    def registrarJugadorAsync(self, totalEsperados: int, context: dict[str, str] | None = None) -> Awaitable[int]:
        return MotorMultijugador._op_registrarJugador.invokeAsync(self, ((totalEsperados, ), context))

    def obtenerCantidadConectados(self, context: dict[str, str] | None = None) -> int:
        return MotorMultijugador._op_obtenerCantidadConectados.invoke(self, ((), context))

    def obtenerCantidadConectadosAsync(self, context: dict[str, str] | None = None) -> Awaitable[int]:
        return MotorMultijugador._op_obtenerCantidadConectados.invokeAsync(self, ((), context))

    def obtenerMaxJugadores(self, context: dict[str, str] | None = None) -> int:
        return MotorMultijugador._op_obtenerMaxJugadores.invoke(self, ((), context))

    def obtenerMaxJugadoresAsync(self, context: dict[str, str] | None = None) -> Awaitable[int]:
        return MotorMultijugador._op_obtenerMaxJugadores.invokeAsync(self, ((), context))

    def colocarBarco(self, idJugador: int, x: int, y: int, context: dict[str, str] | None = None) -> None:
        return MotorMultijugador._op_colocarBarco.invoke(self, ((idJugador, x, y), context))

    def colocarBarcoAsync(self, idJugador: int, x: int, y: int, context: dict[str, str] | None = None) -> Awaitable[None]:
        return MotorMultijugador._op_colocarBarco.invokeAsync(self, ((idJugador, x, y), context))

    def declararListo(self, idJugador: int, context: dict[str, str] | None = None) -> None:
        return MotorMultijugador._op_declararListo.invoke(self, ((idJugador, ), context))

    def declararListoAsync(self, idJugador: int, context: dict[str, str] | None = None) -> Awaitable[None]:
        return MotorMultijugador._op_declararListo.invokeAsync(self, ((idJugador, ), context))

    def todosListos(self, context: dict[str, str] | None = None) -> bool:
        return MotorMultijugador._op_todosListos.invoke(self, ((), context))

    def todosListosAsync(self, context: dict[str, str] | None = None) -> Awaitable[bool]:
        return MotorMultijugador._op_todosListos.invokeAsync(self, ((), context))

    def deQuienEsElTurno(self, context: dict[str, str] | None = None) -> int:
        return MotorMultijugador._op_deQuienEsElTurno.invoke(self, ((), context))

    def deQuienEsElTurnoAsync(self, context: dict[str, str] | None = None) -> Awaitable[int]:
        return MotorMultijugador._op_deQuienEsElTurno.invokeAsync(self, ((), context))

    def disparar(self, idJugador: int, x: int, y: int, context: dict[str, str] | None = None) -> int:
        return MotorMultijugador._op_disparar.invoke(self, ((idJugador, x, y), context))

    def dispararAsync(self, idJugador: int, x: int, y: int, context: dict[str, str] | None = None) -> Awaitable[int]:
        return MotorMultijugador._op_disparar.invokeAsync(self, ((idJugador, x, y), context))

    def obtenerEstadoTablero(self, context: dict[str, str] | None = None) -> list[list[int]]:
        return MotorMultijugador._op_obtenerEstadoTablero.invoke(self, ((), context))

    def obtenerEstadoTableroAsync(self, context: dict[str, str] | None = None) -> Awaitable[list[list[int]]]:
        return MotorMultijugador._op_obtenerEstadoTablero.invokeAsync(self, ((), context))

    def obtenerGanador(self, context: dict[str, str] | None = None) -> int:
        return MotorMultijugador._op_obtenerGanador.invoke(self, ((), context))

    def obtenerGanadorAsync(self, context: dict[str, str] | None = None) -> Awaitable[int]:
        return MotorMultijugador._op_obtenerGanador.invokeAsync(self, ((), context))

    def obtenerMarcador(self, context: dict[str, str] | None = None) -> str:
        return MotorMultijugador._op_obtenerMarcador.invoke(self, ((), context))

    def obtenerMarcadorAsync(self, context: dict[str, str] | None = None) -> Awaitable[str]:
        return MotorMultijugador._op_obtenerMarcador.invokeAsync(self, ((), context))

    @staticmethod
    def checkedCast(
        proxy: ObjectPrx | None,
        facet: str | None = None,
        context: dict[str, str] | None = None
    ) -> MotorMultijugadorPrx | None:
        return checkedCast(MotorMultijugadorPrx, proxy, facet, context)

    @staticmethod
    def checkedCastAsync(
        proxy: ObjectPrx | None,
        facet: str | None = None,
        context: dict[str, str] | None = None
    ) -> Awaitable[MotorMultijugadorPrx | None ]:
        return checkedCastAsync(MotorMultijugadorPrx, proxy, facet, context)

    @overload
    @staticmethod
    def uncheckedCast(proxy: ObjectPrx, facet: str | None = None) -> MotorMultijugadorPrx:
        ...

    @overload
    @staticmethod
    def uncheckedCast(proxy: None, facet: str | None = None) -> None:
        ...

    @staticmethod
    def uncheckedCast(proxy: ObjectPrx | None, facet: str | None = None) -> MotorMultijugadorPrx | None:
        return uncheckedCast(MotorMultijugadorPrx, proxy, facet)

    @staticmethod
    def ice_staticId() -> str:
        return "::Juego::MotorMultijugador"

IcePy.defineProxy("::Juego::MotorMultijugador", MotorMultijugadorPrx)

class MotorMultijugador(Object, ABC):
    """
    Notes
    -----
        The Slice compiler generated this skeleton class from Slice interface ``::Juego::MotorMultijugador``.
    """

    _ice_ids: Sequence[str] = ("::Ice::Object", "::Juego::MotorMultijugador", )
    _op_registrarJugador: IcePy.Operation
    _op_obtenerCantidadConectados: IcePy.Operation
    _op_obtenerMaxJugadores: IcePy.Operation
    _op_colocarBarco: IcePy.Operation
    _op_declararListo: IcePy.Operation
    _op_todosListos: IcePy.Operation
    _op_deQuienEsElTurno: IcePy.Operation
    _op_disparar: IcePy.Operation
    _op_obtenerEstadoTablero: IcePy.Operation
    _op_obtenerGanador: IcePy.Operation
    _op_obtenerMarcador: IcePy.Operation

    @staticmethod
    def ice_staticId() -> str:
        return "::Juego::MotorMultijugador"

    @abstractmethod
    def registrarJugador(self, totalEsperados: int, current: Current) -> int | Awaitable[int]:
        pass

    @abstractmethod
    def obtenerCantidadConectados(self, current: Current) -> int | Awaitable[int]:
        pass

    @abstractmethod
    def obtenerMaxJugadores(self, current: Current) -> int | Awaitable[int]:
        pass

    @abstractmethod
    def colocarBarco(self, idJugador: int, x: int, y: int, current: Current) -> None | Awaitable[None]:
        pass

    @abstractmethod
    def declararListo(self, idJugador: int, current: Current) -> None | Awaitable[None]:
        pass

    @abstractmethod
    def todosListos(self, current: Current) -> bool | Awaitable[bool]:
        pass

    @abstractmethod
    def deQuienEsElTurno(self, current: Current) -> int | Awaitable[int]:
        pass

    @abstractmethod
    def disparar(self, idJugador: int, x: int, y: int, current: Current) -> int | Awaitable[int]:
        pass

    @abstractmethod
    def obtenerEstadoTablero(self, current: Current) -> Sequence[Sequence[int] | Buffer] | Awaitable[Sequence[Sequence[int] | Buffer]]:
        pass

    @abstractmethod
    def obtenerGanador(self, current: Current) -> int | Awaitable[int]:
        pass

    @abstractmethod
    def obtenerMarcador(self, current: Current) -> str | Awaitable[str]:
        pass

MotorMultijugador._op_registrarJugador = IcePy.Operation(
    "registrarJugador",
    "registrarJugador",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0),),
    (),
    ((), IcePy._t_int, False, 0),
    ())

MotorMultijugador._op_obtenerCantidadConectados = IcePy.Operation(
    "obtenerCantidadConectados",
    "obtenerCantidadConectados",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), IcePy._t_int, False, 0),
    ())

MotorMultijugador._op_obtenerMaxJugadores = IcePy.Operation(
    "obtenerMaxJugadores",
    "obtenerMaxJugadores",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), IcePy._t_int, False, 0),
    ())

MotorMultijugador._op_colocarBarco = IcePy.Operation(
    "colocarBarco",
    "colocarBarco",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0), ((), IcePy._t_int, False, 0), ((), IcePy._t_int, False, 0)),
    (),
    None,
    ())

MotorMultijugador._op_declararListo = IcePy.Operation(
    "declararListo",
    "declararListo",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0),),
    (),
    None,
    ())

MotorMultijugador._op_todosListos = IcePy.Operation(
    "todosListos",
    "todosListos",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), IcePy._t_bool, False, 0),
    ())

MotorMultijugador._op_deQuienEsElTurno = IcePy.Operation(
    "deQuienEsElTurno",
    "deQuienEsElTurno",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), IcePy._t_int, False, 0),
    ())

MotorMultijugador._op_disparar = IcePy.Operation(
    "disparar",
    "disparar",
    OperationMode.Normal,
    None,
    (),
    (((), IcePy._t_int, False, 0), ((), IcePy._t_int, False, 0), ((), IcePy._t_int, False, 0)),
    (),
    ((), IcePy._t_int, False, 0),
    ())

MotorMultijugador._op_obtenerEstadoTablero = IcePy.Operation(
    "obtenerEstadoTablero",
    "obtenerEstadoTablero",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), _Juego_Matriz_t, False, 0),
    ())

MotorMultijugador._op_obtenerGanador = IcePy.Operation(
    "obtenerGanador",
    "obtenerGanador",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), IcePy._t_int, False, 0),
    ())

MotorMultijugador._op_obtenerMarcador = IcePy.Operation(
    "obtenerMarcador",
    "obtenerMarcador",
    OperationMode.Normal,
    None,
    (),
    (),
    (),
    ((), IcePy._t_string, False, 0),
    ())

__all__ = ["MotorMultijugador", "MotorMultijugadorPrx", "_Juego_MotorMultijugadorPrx_t"]
