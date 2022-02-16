from ctypes import *
from enum import Enum
import os
import time
from threading import *
import threading
import inspect  # Angabe der Zeilennumern

# Arbeitsablauf fuer die Verbindung zu Virtuos
# 1.  !! Init DLL
# 2.  Starte VirtuosM und VirtuosV
# 3.  !! Festlegen der CORBA Informationen fuer den Server
# 4.  !! Starte die Verbindung mit dem CORBA-Server
# 5.  Lade VirtuosM-Projekt
# 6.  Ramp up the project
# 7.  Run self.virtuosM
# 8.  !! Starte das zyklische Update und das Update des current set
# 9.  Lese einen Port
#     Schreibe einen Port
#     Aendere einen Parameter
#     Aendere eine Eigenschaft eines Blockbausteins
# 10. !! Stoppe das zyklische Update und das Update des current set
# 11. Stoppe die Simulation
# 12. Ramp down the project
# 13. Schliesse das Projekt in VirtuosM
# 11. !! Detach DLL
# !! notwendige Schritte, andere Schritte koennen evtl. uebersprungen werden
# Pfade in Virtuos werden als Strin in hierarchischer Punktnotation uebergeben
# Bsp. "[Hauptblock].[Unterblock].[Port]"
# Die Funktionen geben in der Regel den Status (Erfolg = 0, Misserfolg = -1) zurueck.


class ValueID(Structure):
    """
    Komplexer Datentyp, der die notwendigen Infos enthaelt, um auf die IO-Ports der Simulationsbloecke 
    zuzugreifen 
    """
    _fields_ = [('valueID', c_int32),
                ('interfaceID', c_int32),
                ('interfaceID2', c_int32),
                ('valueDataType', c_int32),
                ('valueIOType', c_uint32)]


class VIODataType(Enum):
    # Datentypen fuer Virtuos
    V_IO_TYPE_UNKNOWN   = 0x0000
    V_IO_TYPE_BOOLEAN   = 0x0001
    V_IO_TYPE_REAL32    = 0x0002
    V_IO_TYPE_REAL64    = 0x0004
    V_IO_TYPE_STRING    = 0x0008
    V_IO_TYPE_INT8      = 0x0010
    V_IO_TYPE_INT16     = 0x0020
    V_IO_TYPE_INT32     = 0x0040
    V_IO_TYPE_INT64     = 0x0080
    V_IO_TYPE_UINT8     = 0x0100
    V_IO_TYPE_UINT16    = 0x0200
    V_IO_TYPE_UINT32    = 0x0400
    V_IO_TYPE_UINT64    = 0x0800
    V_IO_TYPE_WSTRING   = 0x2000
    V_IO_TYPE_UUID      = 0x4000
    V_IO_TYPE_EVENT     = 0x8000
    V_IO_TYPE_C_POINTER = 0x20000


class VIOAccessType(Enum):
    V_IO_ACCESS_READ = 0x0001
    V_IO_ACCESS_WRITE = 0x0002


class ForceType(Enum):
    V_NONE = 0
    V_FORCE = 1  # ! Used to enable forcing of a value in ICommunication::setForced.
    V_RELEASE = 2  # ! Used to disable forcing of a value in ICommunication::setForced.
    V_WRITE_FORCED = 3  # ! Used in the write-Methods of ICommunication to indicate that the value should be written
    # to the "forced" value of a solver variable is disabled.
    V_WRITE_UNFORCED = 4  # ! Used in the write-Methods of ICommunication to indicate that the value should be written
    # to the "unforced" value of a solver variable.


class StatusException(Exception):
    """Raise when status = V_DAMGD"""
    def __init__(self, *args):
        self.message = "A status error was raised. Eine Funktion von VirtuosZugriff konnte nicht ausgefuehrt werden."


# aktuelle Zeilennumer ausgeben
def lineno():
    return inspect.currentframe().f_back.f_lineno


class VirtuosZugriff():
    def __init__(self):
        # lokale Variablen
        self.status = None
        self.ipCorba = None
        self.portCorba = None
        self.serverNameCorba = None
        self.parameterValueID = None
        self.nwd = None
        self.oldDirectory = os.getcwd()
        self.libDll = "C:\\Virtuos_V_2_5_x64\\bin_x64\\self.virtuos_interface_x64.dll"
        self.pathVirtuosM = "C:\\Virtuos_V_2_5_x64\\bin_x64\\VirtuosM_x64.exe"
        self.pathVirtuosV = "C:\\Virtuos_V_2_5_x64\\bin_x64\\VirtuosV_x64.exe"
        self.projectVirtuosM = None
        self.pathToSave = None  # Speicherort des Virtuos-Projekts
        self.prozessIDV = c_int64()  # ProzessID von VirtuosV
        self.prozessIDM = c_int64()  # ProzessID von VirtuosM
        self.leseparameter = None
        self.schreibparameter = None  # zu schreibende Parameter
        self.maxBufferLen = None
        self.remainingSets = None
        self.bufferFillState = None
        self.continueUpdate = 0  # Endkriterium fuer Update des CurrentSet
        # Schloss zum vollständigen Durchführen einer Funktion ohne Unterbrechung
        self.lock = threading.RLock()
        self.vi = None  # Verbindung zur Virtuos-DLL

    ## Definition allgemeiner Variablen
    V_SUCCD = 0
    V_DAMGD = -1

    ## Definition von allgemeinen Funktionen
    def stringToCharP(self, string):  # Umwandlung von string zu c_char_p
        y = c_char_p(string.encode('utf-8'))
        return y

    def strToByte(self, string):  # Umwandlung von string zu byte
        y = string.encode('utf-8')
        return y

    ### Virtuos-Funktionen
    ## Virtuos-Schnittstelle
    # initDLL
    def virtuosDLL(self, nwd="C:\\Virtuos_V_2_5_x64\\bin_x64",
                   libDll="C:\\Virtuos_V_2_5_x64\\bin_x64\\self.virtuos_interface_x64.dll"):
        # global self.vi
        self.nwd = nwd
        self.libDll = libDll
        self.oldDirectory = os.getcwd()
        os.chdir(self.nwd)  # Aenderung des work directory, damit dort ausgefuehrt wird, wo die DLL liegt
        # mydll = cdll.LoadLibrary(self.libDll)
        # evtl Abhaengigkeiten von anderen DLLs, die nicht gefunden werden
        self.vi = cdll.virtuos_interface_x64
        cdll.virtuos_interface_x64.initDLL()

    # set CORBA-information
    def corbaInfo(self, ipCorba="127.0.0.1", portCorba="54335", serverNameCorba="Visualization"):
        self.ipCorba = ipCorba
        self.ipCorba = c_char_p(self.ipCorba.encode('utf-8'))
        self.portCorba = portCorba
        self.portCorba = self.stringToCharP(self.portCorba)
        self.serverNameCorba = serverNameCorba
        self.serverNameCorba = self.stringToCharP(self.serverNameCorba)
        if (cdll.virtuos_interface_x64.setCorbaInfo(self.ipCorba, self.portCorba, self.serverNameCorba) == 0):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    # start VirtuosM
    def virtuosM(self, pathVirtuosM="C:\\Virtuos_V_2_5_x64\\bin_x64\\VirtuosM_x64.exe"):
        self.pathVirtuosM = pathVirtuosM
        # gleichzeitiger Verbindungsaufbau mit CORBA-Server
        virtuosparameter = "-startcorbaserver"
        virtuosparameter = (c_char_p * 1)(virtuosparameter.encode('utf-8'))
        if (self.vi.startVirtuosM(self.stringToCharP(self.pathVirtuosM), c_int32(1), virtuosparameter,
                                  pointer(self.prozessIDM)) == 0):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    # start VirtuosV
    # Soll kein Projekt geoeffnet werden: pathProjektVirtuosV = None
    # Wird ein Prokekt auf diese Weise geöffnet, kann es nur ueber killProcess mit der Projekt ID geschlossen werden
    # Startet gleichzeitig Simulation
    def virtuosV(self, pathProjectVirtuosV, pathVirtuosV="C:\\Virtuos_V_2_5_x64\\bin_x64\\VirtuosV_x64.exe"):
        self.pathVirtuosV = pathVirtuosV
        if pathProjectVirtuosV is None:
            # Soll kein Projekt geoeffnet werden, ist kein Parameter notwendig
            virtuosparameter = None
        else:
            virtuospar = ["-s", pathProjectVirtuosV]
            virtuosparameter = (c_char_p * 2)()
            virtuosparameter[0] = virtuospar[0].encode('utf-8')
            virtuosparameter[1] = virtuospar[1].encode('utf-8')
        self.pathVirtuosV = self.stringToCharP(self.pathVirtuosV)
        argVirtuosV = c_int(len(virtuosparameter))
        if (self.vi.startVirtuosV(self.pathVirtuosV, argVirtuosV, virtuosparameter, pointer(self.prozessIDV)) == 0):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    # Corba-Verbindung aufbauen
    def connectionCorba(self):
        if (self.vi.startConnection() == 0):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    # Verbindung ueberpruefen
    def isConnected(self):
        if (self.vi.connected() == 0):
            return VirtuosZugriff.V_SUCCD
        else:
            return VirtuosZugriff.V_DAMGD

    # DLL trennen
    def unloadDLL(self):
        try:
            self.vi.detachDLL()
        except:
            pass

    # Beenden des Prozesses
    def stopProcess(self, prozessID):
        if (self.vi.terminateProcess(prozessID) == 0):
            return VirtuosZugriff.V_SUCCD
        else:
            return VirtuosZugriff.V_DAMGD

    # Hartes Beenden des Prozesses
    def killProcess(self, prozessID):
        if (self.vi.killProcess(prozessID) == 0):
            return VirtuosZugriff.V_SUCCD
        else:
            return VirtuosZugriff.V_DAMGD

    # Zustand des Prozesses
    def stateProcess(self, prozessIDM):
        prozesszustand = c_long()
        if (self.vi.processState(prozessIDM, pointer(prozesszustand)) == 0):
            return VirtuosZugriff.V_SUCCD, prozesszustand
        else:
            return VirtuosZugriff.V_DAMGD, prozesszustand

    ## Projekt-Schnittstelle
    # Projekt in VirtuosM laden
    def getProjectM(self, projectVirtuosM,
                    convert=1):
        self.projectVirtuosM = projectVirtuosM
        dconvert = convert
        if (self.vi.loadProject(self.stringToCharP(self.projectVirtuosM), dconvert) == 0):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    # Ueberpruefen, ob ein Projekt in VirtuosM geoeffnet ist
    def isOpen(self):
        if (self.vi.isOpened() == 0):
            return VirtuosZugriff.V_SUCCD
        else:
            return VirtuosZugriff.V_DAMGD

    # Projekt in VirtuosM schliessen
    def closeProjectM(self):
        if (self.vi.closeProject() == 0):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    # Projekt in VirtuosM speichern
    def saveVirtuosMAs(self, pathToSave):
        self.pathToSave = pathToSave
        if (self.vi.saveProjectAs(self.stringToCharP(self.pathToSave)) == VirtuosZugriff.V_SUCCD):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    # Merge Projekt
    def mergeProject(self, pathToEcf, assemblyName):
        if (self.vi.merge(self.stringToCharP(pathToEcf), self.stringToCharP(assemblyName)) == VirtuosZugriff.V_SUCCD):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    ## Simulations-Schnittstelle
    # Ramp Up der Simulation
    def rampUpSim(self):
        if (self.vi.rampUp() == 0):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    # Ramp Down der Simulation
    def rampDownSim(self):
        if (self.vi.rampDown() == VirtuosZugriff.V_SUCCD):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    # Starten der Simulation
    def startSim(self):
        if (self.vi.run() == VirtuosZugriff.V_SUCCD):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    # Beenden der Simulation
    def stopSim(self):
        if (self.vi.stop() == VirtuosZugriff.V_SUCCD):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    # Ein Schritt der Simulation
    def simStep(self):
        if (self.vi.step() == VirtuosZugriff.V_SUCCD):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    # Reset der Simulation
    def simReset(self):
        if (self.vi.reset() == VirtuosZugriff.V_SUCCD):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    # Abfrage des Simulationszustands
    def simStatus(self):
        simZustand = c_char()
        groesse = c_uint32(50)
        if (self.vi.getSimulationStatus(pointer(simZustand), pointer(groesse)) == VirtuosZugriff.V_SUCCD):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        simZustand = (simZustand.value).decode("utf-8")
        groesse = groesse.value
        return self.status, simZustand, groesse

    ## Modell-Schnittstelle
    # Eigenschaft eines Projektbaustein aendern
    def propertyBlock(self, pathBlock="[ML_Anwendungsfall_MF].[Materialflussanlage].[Enable Corba Transmission]",
                      propertyValue="1"):
        # Es koennen nur Eigenschaften geaendert werden, die als property in einem Bustein vorhanden sind
        dpathBlock = pathBlock
        dpropertyValue = propertyValue
        if (self.vi.setProperty(self.stringToCharP(dpathBlock), self.stringToCharP(dpropertyValue))
                == VirtuosZugriff.V_SUCCD):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    # Parameter eines Projektbausteins aendern
    def parameterBlock(self, parameterName, parameterValue):
        dparameterName = self.stringToCharP(parameterName)  # Parametername in hierachischer Punktnotation
        dparameterValue = self.stringToCharP(parameterValue)  # Wert als String uebergeben
        if (self.vi.setParameter(dparameterName, dparameterValue)):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    ## Kommunikations-Schnittstelle
    # ValueID der Parameter, Rueckgabe: status und ValueID
    def readValueID(self, parameterPfad, dataType=None):
        # evtl. Umwandlung in Liste
        if not isinstance(parameterPfad, list) and not isinstance(parameterPfad, tuple):
            parameterPfad = [parameterPfad]
        # Umwandlung des Parameterpfads in Ctypes
        dparameterPfad = (c_char_p * len(parameterPfad))()
        for i in range(0, len(dparameterPfad)):
            dparameterPfad[i] = self.strToByte(parameterPfad[i])
        self.parameterValueID = (ValueID * len(dparameterPfad))()
        # Default datentyp ist REAL64
        if dataType is None:
            ddataType = [VIODataType.V_IO_TYPE_REAL64.value] * len(dparameterPfad)
        else:
            ddataType = dataType.copy()
        self.status = -1
        # Iteration ueber alle Parameter
        for ipara in range(0, len(dparameterPfad)):
            # Es werden alle ValueIDs mit lesendem Zugriff bestimmt: ACCESS_READ
            # Dies funktioniert auch bei verbundenen Ports.
            # Die ValueIDs koennen trotzdem zum Schreiben benutzt werden.
            if (self.vi.getValueID(dparameterPfad[ipara], ddataType[ipara], VIOAccessType.V_IO_ACCESS_READ.value,
                                   pointer(self.parameterValueID[ipara])) == VirtuosZugriff.V_SUCCD):
                nr = ipara + 1
                self.status = VirtuosZugriff.V_SUCCD
            else:
                self.status = VirtuosZugriff.V_DAMGD
                # Die ValueID wird als Structure zurueck gegeben
        return self.status, self.parameterValueID

    # Parameter lesen, Rueckgabe: status und Parameterwert
    def readValue(self, parameterValueID, dataType=None):
        with self.lock:
            # Kopie, wenn ein mutuable vorliegt
            try:
                dparameterValueID = parameterValueID
            except AttributeError:
                dparameterValueID = parameterValueID
            # Umwandlung in Liste, wenn noch nicht vorhanden
            try:
                a = dparameterValueID[0]
            except TypeError:
                dparameterValueID = (ValueID * 1)()
                dparameterValueID[0] = parameterValueID
            except:
                pass
            leseparameter = [None] * len(dparameterValueID)
            # Default Datentyp ist REAL64
            if dataType is None:
                ddataType = [VIODataType.V_IO_TYPE_REAL64] * len(dparameterValueID)
            else:
                ddataType = dataType.copy()
            nr = 0
            ivalueID = -1
            # Schleife ueber alle ValueIDs
            for valueID in dparameterValueID:
                ivalueID += 1
                nr += 1
                try:
                    # Lesen der unterschiedlichen Datentypen
                    if (ddataType[ivalueID] == VIODataType.V_IO_TYPE_REAL64):
                        dleseparametera = c_double(0)
                        if (self.vi.readReal64Value(dparameterValueID[ivalueID], pointer(dleseparametera)) ==
                                VirtuosZugriff.V_SUCCD):
                            leseparameter[ivalueID] = dleseparametera
                            self.status = VirtuosZugriff.V_SUCCD
                        else:
                            self.status = VirtuosZugriff.V_DAMGD
                    elif (ddataType[ivalueID] == VIODataType.V_IO_TYPE_BOOLEAN):
                        dleseparametera = c_bool(0)
                        if (self.vi.readBooleanValue(dparameterValueID[ivalueID], pointer(dleseparametera)) ==
                                VirtuosZugriff.V_SUCCD):
                            leseparameter[ivalueID] = dleseparametera
                            self.status = VirtuosZugriff.V_SUCCD
                        else:
                            self.status = VirtuosZugriff.V_DAMGD
                    elif (ddataType[ivalueID] == VIODataType.V_IO_TYPE_REAL32):
                        dleseparametera = c_double(0)
                        if (self.vi.readReal32Value(dparameterValueID[ivalueID], pointer(dleseparametera)) ==
                                VirtuosZugriff.V_SUCCD):
                            leseparameter[ivalueID] = dleseparametera
                            self.status = VirtuosZugriff.V_SUCCD
                        else:
                            self.status = VirtuosZugriff.V_DAMGD
                    elif (ddataType[ivalueID] == VIODataType.V_IO_TYPE_UINT8):
                        dleseparametera = c_uint(0)
                        if (self.vi.readUInt8Value(dparameterValueID[ivalueID], pointer(dleseparametera)) ==
                                VirtuosZugriff.V_SUCCD):
                            leseparameter[ivalueID] = dleseparametera
                            self.status = VirtuosZugriff.V_SUCCD
                        else:
                            self.status = VirtuosZugriff.V_DAMGD
                    elif (ddataType[ivalueID] == VIODataType.V_IO_TYPE_INT8):
                        dleseparametera = c_int(0)
                        if (self.vi.readInt8Value(dparameterValueID[ivalueID],
                                                  pointer(dleseparametera)) == VirtuosZugriff.V_SUCCD):
                            leseparameter[ivalueID] = dleseparametera
                            self.status = VirtuosZugriff.V_SUCCD
                        else:
                            self.status = VirtuosZugriff.V_DAMGD
                    elif (ddataType[ivalueID] == VIODataType.V_IO_TYPE_UINT16):
                        dleseparametera = c_uint(0)
                        if (self.vi.readUInt16Value(dparameterValueID[ivalueID], pointer(dleseparametera)) ==
                                VirtuosZugriff.V_SUCCD):
                            leseparameter[ivalueID] = dleseparametera
                            self.status = VirtuosZugriff.V_SUCCD
                        else:
                            self.status = VirtuosZugriff.V_DAMGD
                    elif (ddataType[ivalueID] == VIODataType.V_IO_TYPE_INT16):
                        dleseparametera = c_int(0)
                        if (self.vi.readInt16Value(dparameterValueID[ivalueID], pointer(dleseparametera)) ==
                                VirtuosZugriff.V_SUCCD):
                            leseparameter[ivalueID] = dleseparametera
                            self.status = VirtuosZugriff.V_SUCCD
                        else:
                            self.status = VirtuosZugriff.V_DAMGD
                    elif (ddataType[ivalueID] == VIODataType.V_IO_TYPE_UINT32):
                        dleseparametera = c_uint(0)
                        if (self.vi.readUInt32Value(dparameterValueID[ivalueID], pointer(dleseparametera)) ==
                                VirtuosZugriff.V_SUCCD):
                            leseparameter[ivalueID] = dleseparametera
                            self.status = VirtuosZugriff.V_SUCCD
                        else:
                            self.status = VirtuosZugriff.V_DAMGD
                    elif (ddataType[ivalueID] == VIODataType.V_IO_TYPE_INT32):
                        dleseparametera = c_int(0)
                        if (self.vi.readInt32Value(dparameterValueID[ivalueID], pointer(dleseparametera)) ==
                                VirtuosZugriff.V_SUCCD):
                            leseparameter[ivalueID] = dleseparametera
                            self.status = VirtuosZugriff.V_SUCCD
                        else:
                            self.status = VirtuosZugriff.V_DAMGD
                    elif (ddataType[ivalueID] == VIODataType.V_IO_TYPE_UINT64):
                        dleseparametera = c_uint(0)
                        if (self.vi.readUInt64Value(dparameterValueID[ivalueID], pointer(dleseparametera)) ==
                                VirtuosZugriff.V_SUCCD):
                            leseparameter[ivalueID] = dleseparametera
                            self.status = VirtuosZugriff.V_SUCCD
                        else:
                            self.status = VirtuosZugriff.V_DAMGD
                    elif (ddataType[ivalueID] == VIODataType.V_IO_TYPE_INT64):
                        dleseparametera = c_int(0)
                        if (self.vi.readInt64Value(dparameterValueID[ivalueID], pointer(dleseparametera)) ==
                                VirtuosZugriff.V_SUCCD):
                            leseparameter[ivalueID] = dleseparametera
                            self.status = VirtuosZugriff.V_SUCCD
                        else:
                            self.status = VirtuosZugriff.V_DAMGD
                    elif (ddataType[ivalueID] == VIODataType.V_IO_TYPE_STRING):
                        dleseparametera = c_char(0)
                        self.maxBufferLen = (c_uint * len(dparameterValueID))(100)
                        dmaxBufferLena = c_uint(0)
                        if (self.vi.readStringValue(dparameterValueID[ivalueID], pointer(dleseparametera),
                                                    pointer(dmaxBufferLena)) == VirtuosZugriff.V_SUCCD):
                            leseparameter[ivalueID] = dleseparametera
                            self.maxBufferLen[ivalueID] = dmaxBufferLena
                            self.status = VirtuosZugriff.V_SUCCD
                        else:
                            self.status = VirtuosZugriff.V_DAMGD
                    else:
                        self.status = VirtuosZugriff.V_DAMGD
                except:
                    pass
        # Umwandlung der ctypes
        for jleseparameter in range(0, len(leseparameter)):
            try:
                leseparameter[jleseparameter] = (leseparameter[jleseparameter]).value
            except:
                leseparameter[jleseparameter] = None
        return self.status, leseparameter

    # Parameter schreiben
    def writeValue(self, parameterValueID, schreibparameter, dataType=None):
        # Kopie, wenn ein mutuable vorliegt
        try:
            lparameterValueID = parameterValueID.copy()
        except AttributeError:
            lparameterValueID = parameterValueID
        # Umwandlung in Liste, wenn noch nicht vorhanden
        try:
            a = lparameterValueID[0]
        except TypeError:
            lparameterValueID = (ValueID * 1)()
            lparameterValueID[0] = parameterValueID.copy()
        except:
            pass
        # Ports forcen, bevor sie beschrieben werden
        self.status = self.forcePorts(lparameterValueID)
        # Schreibparameter in Liste umwandeln
        if not isinstance(schreibparameter, list):
            self.schreibparameter = [schreibparameter]
        else:
            self.schreibparameter = schreibparameter[:]
        # Default Datentyp ist REAL64
        if dataType is None:
            ddataType = [VIODataType.V_IO_TYPE_REAL64] * len(self.parameterValueID)
        else:
            ddataType = dataType.copy()
        # Iteration ueber alle zu schreibenden Parameter
        for i in range(0, len(self.schreibparameter)):
            nr = i + 1
            # Unterscheidung der Datentypen
            if (ddataType[i] == VIODataType.V_IO_TYPE_REAL64):
                if (self.vi.writeReal64Value(lparameterValueID[i], c_double(self.schreibparameter[i]),
                                             ForceType.V_WRITE_FORCED.value) == VirtuosZugriff.V_SUCCD):
                    self.status = VirtuosZugriff.V_SUCCD
                else:
                    self.status = VirtuosZugriff.V_DAMGD
            elif (ddataType[i] == VIODataType.V_IO_TYPE_BOOLEAN):
                if (self.vi.writeBooleanValue(lparameterValueID[i], c_bool(self.schreibparameter[i]),
                                              ForceType.V_WRITE_FORCED.value) == VirtuosZugriff.V_SUCCD):
                    self.status = VirtuosZugriff.V_SUCCD
                else:
                    self.status = VirtuosZugriff.V_DAMGD
            elif (ddataType[i] == VIODataType.V_IO_TYPE_REAL32):
                if (self.vi.writeReal32Value(lparameterValueID[i], c_double(self.schreibparameter[i]),
                                             ForceType.V_WRITE_FORCED.value) == VirtuosZugriff.V_SUCCD):
                    self.status = VirtuosZugriff.V_SUCCD
                else:
                    self.status = VirtuosZugriff.V_DAMGD
            elif (ddataType[i] == VIODataType.V_IO_TYPE_UINT8):
                if (self.vi.writeUInt8Value(lparameterValueID[i], c_uint(self.schreibparameter[i]),
                                            ForceType.V_WRITE_FORCED.value) == VirtuosZugriff.V_SUCCD):
                    self.status = VirtuosZugriff.V_SUCCD
                else:
                    self.status = VirtuosZugriff.V_DAMGD
            elif (ddataType[i] == VIODataType.V_IO_TYPE_UINT16):
                if (self.vi.writeUInt16Value(lparameterValueID[i], c_uint(self.schreibparameter[i]),
                                             ForceType.V_WRITE_FORCED.value) == VirtuosZugriff.V_SUCCD):
                    self.status = VirtuosZugriff.V_SUCCD
                else:
                    self.status = VirtuosZugriff.V_DAMGD
            elif (ddataType[i] == VIODataType.V_IO_TYPE_UINT32):
                if (self.vi.writeUInt32Value(lparameterValueID[i], c_uint(self.schreibparameter[i]),
                                             ForceType.V_WRITE_FORCED.value) == VirtuosZugriff.V_SUCCD):
                    self.status = VirtuosZugriff.V_SUCCD
                else:
                    self.status = VirtuosZugriff.V_DAMGD
            elif (ddataType[i] == VIODataType.V_IO_TYPE_UINT64):
                if (self.vi.writeUInt64Value(lparameterValueID[i], c_uint(self.schreibparameter[i]),
                                             ForceType.V_WRITE_FORCED.value) == VirtuosZugriff.V_SUCCD):
                    self.status = VirtuosZugriff.V_SUCCD
                else:
                    self.status = VirtuosZugriff.V_DAMGD
            elif (ddataType[i] == VIODataType.V_IO_TYPE_INT8):
                if (self.vi.writeInt8Value(lparameterValueID[i], c_int(self.schreibparameter[i]),
                                           ForceType.V_WRITE_FORCED.value) == VirtuosZugriff.V_SUCCD):
                    self.status = VirtuosZugriff.V_SUCCD
                else:
                    self.status = VirtuosZugriff.V_DAMGD
            elif (ddataType[i] == VIODataType.V_IO_TYPE_INT16):
                if (self.vi.writeInt16Value(lparameterValueID[i], c_int(self.schreibparameter[i]),
                                            ForceType.V_WRITE_FORCED.value) == VirtuosZugriff.V_SUCCD):
                    self.status = VirtuosZugriff.V_SUCCD
                else:
                    self.status = VirtuosZugriff.V_DAMGD
            elif (ddataType[i] == VIODataType.V_IO_TYPE_INT32):
                if (self.vi.writeInt32Value(lparameterValueID[i], c_int(self.schreibparameter[i]),
                                            ForceType.V_WRITE_FORCED.value) == VirtuosZugriff.V_SUCCD):
                    self.status = VirtuosZugriff.V_SUCCD
                else:
                    self.status = VirtuosZugriff.V_DAMGD
            elif (ddataType[i] == VIODataType.V_IO_TYPE_INT64):
                if (self.vi.writeInt64Value(lparameterValueID[i], c_int(self.schreibparameter[i]),
                                            ForceType.V_WRITE_FORCED.value) == VirtuosZugriff.V_SUCCD):
                    self.status = VirtuosZugriff.V_SUCCD
                else:
                    self.status = VirtuosZugriff.V_DAMGD
            elif (ddataType[i] == VIODataType.V_IO_TYPE_STRING):
                if (self.vi.writeStringValue(lparameterValueID[i], c_char_p(self.schreibparameter[i]),
                                             ForceType.V_WRITE_FORCED.value) == VirtuosZugriff.V_SUCCD):
                    self.status = VirtuosZugriff.V_SUCCD
                else:
                    self.status = VirtuosZugriff.V_DAMGD
            else:
                self.status = VirtuosZugriff.V_DAMGD
        return self.status

    # Force Ports
    def forcePorts(self, parameterValueID):
        # Ueberpruefen, ob Array oder List uebergeben ist; ansonsten umwandeln
        # Kopie, falls ein mutuable vorliegt
        try:
            a = parameterValueID[0]
            if isinstance(parameterValueID, tuple):
                dparameterValueID = parameterValueID
            else:
                dparameterValueID = parameterValueID
        except TypeError:
            dparameterValueID = (ValueID * 1)()
            if isinstance(parameterValueID, tuple):
                dparameterValueID[0] = parameterValueID
            else:
                dparameterValueID[0] = parameterValueID.copy()
        except:
            pass
        # Iteration ueber alle Parameter
        for i in range(0, len(dparameterValueID)):
            nr = i + 1
            if (self.vi.setForced(dparameterValueID[i], ForceType.V_FORCE.value) == VirtuosZugriff.V_SUCCD):
                self.status = VirtuosZugriff.V_SUCCD
            else:
                self.status = VirtuosZugriff.V_DAMGD
        return self.status

    # Unforce aller Ports
    def unforcePorts(self):
        if (self.vi.unforceAll() == VirtuosZugriff.V_SUCCD):
            self.status = VirtuosZugriff.V_SUCCD
        else:
            self.status = VirtuosZugriff.V_DAMGD
        return self.status

    ## Update
    # Starten des zyklischen Updates, update rate in ms
    def startUpdate(self, updateRate=10):
        # vorhandene Anzahl an Datensets
        self.remainingSets = c_int32(0)
        self.bufferFillState = c_long(0)
        if (self.vi.startCyclicUpdate(updateRate) == VirtuosZugriff.V_SUCCD):
            self.continueUpdate = 1  # Endkriterium fuer das Update des CurrentSet
            time.sleep(0.03)  # wichtig: Pause vor dem ersten Update des CurrentSet ist notwendig
            self.vi.updateCurrentSet(pointer(self.remainingSets), pointer(self.bufferFillState))
            # Thread fuer das kontinuierliche Update des CurrentSet im Hintergrund
            t = Thread(target=self.startUpdateCurrentSet, args=(updateRate,))
            t.start()  # Start des Threads
        else:
            self.continueUpdate = 0

    # Starten des zyklischen Updates ohne CurrentSet, update rate in ms
    # CurrentSet muss getrennt gestartet werden
    def startZyklUpdate(self, updateRate=10):
        # vorhandene Anzahl an Datensets
        self.remainingSets = c_int32(0)
        self.bufferFillState = c_long(0)
        if (self.vi.startCyclicUpdate(updateRate) == VirtuosZugriff.V_SUCCD):
            self.continueUpdate = 1
            time.sleep(0.03)  # wichtig: Pause vor dem ersten Update des CurrentSet ist notwendig
        else:
            # Abbruchkriterium fuer CurrenSet, dessen Update nicht ohne zyklisches Update stattfinden kann
            self.continueUpdate = 0

    # Starten des Updates des CurrentSet
    def startUpdateCurrentSet(self, updateRate):
        while (self.continueUpdate == 1):
            if (self.vi.updateCurrentSet(pointer(self.remainingSets), pointer(self.bufferFillState)) ==
                    VirtuosZugriff.V_SUCCD):
                self.status = VirtuosZugriff.V_SUCCD
            else:
                self.status = VirtuosZugriff.V_DAMGD
            # Update des CurrentSet in aehnlicher Haeufigkeit wie zyklisches Update
            if self.remainingSets.value == 0:
                time.sleep((updateRate / 1000) * 1)
        return self.status

    # Stop des zyklischen Updates
    def stopUpdate(self):
        self.status = self.vi.stopCyclicUpdate()
        # Endsignal fuer Update des CurrentSet
        self.continueUpdate = 0
        return self.status, self.continueUpdate


""" 
Hier nicht definierte Funktionen, die in der DLL enthalten sind:
VRESULT getClientID(char* o_clientID, V_UINT32 *io_size);
VRESULT saveProject();
VRESULT setSolverType(const char *i_solverType);
VRESULT getProjectName(char* o_loadedFileName, V_UINT32 *io_size);
VRESULT readChangedStringValue(const ValueID i_id, char *o_value, V_UINT32 *io_size, V_BOOLEAN *o_changed);
VRESULT setBuffered(V_BOOLEAN i_buffered, V_INT32 i_maxFiFoSize = 10000);
VRESULT index(V_INT32 i_row, V_INT32 i_column, ModelIndex *i_parentIndex, ModelIndex *o_childIndex);
VRESULT rowCount(ModelIndex *i_parentIndex, V_INT32 *o_count);
VRESULT columnCount(ModelIndex *i_parentIndex, V_INT32 *o_count);
VRESULT getData(ModelIndex *i_index, V_INT32 i_role, char* o_data, V_UINT32 *io_size);
VRESULT parent(ModelIndex *i_index, ModelIndex *o_parentIndex)
"""
