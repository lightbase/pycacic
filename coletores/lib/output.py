# -*- coding: UTF-8 -*-

"""

    Copyright 2000, 2001, 2002, 2003, 2004, 2005 Dataprev - Empresa de Tecnologia e Informações da Previdência Social, Brasil
    
    Este arquivo é parte do programa CACIC - Configurador Automático e Coletor de Informações Computacionais
    
    O CACIC é um software livre você pode redistribui-lo e/ou modifica-lo dentro dos termos da Licença Pública Geral GNU como 
    publicada pela Fundação do Software Livre (FSF) na versão 2 da Licença, ou (na sua opnião) qualquer versão.
    
    Este programa é distribuido na esperança que possa ser  util, mas SEM NENHUMA GARANTIA sem uma garantia implicita de ADEQUAÇÂO a qualquer
    MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral GNU para maiores detalhes.
    
    Você deve ter recebido uma cópia da Licença Pública Geral GNU, sob o título "LICENCA.txt", junto com este programa, se não, escreva para a Fundação do Software
    Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


    Modulo computador from Linux
    
    Modulo com finalidade de montar o arquivo
    de saída do agente.
    
    ------
    @author: Breno Brito - DF
    @version: ? (13 de setembro de 2013)
    
"""


from computador import *

DEFAULT_STRING_VALUE = ''

class Win32_Keyboard:
 """-> Represents a keyboard installed on a computer system running Windows."""
    def __init__(self):
        self.Availability = 0
        self.Caption = DEFAULT_STRING_VALUE
        self.Description = DEFAULT_STRING_VALUE
        # datetime InstallDate
        self.Manufacturer = DEFAULT_STRING_VALUE
        self.Name = DEFAULT_STRING_VALUE

    # desc Availability
    # string Caption
    # string Description
    # datetime InstallDate
    # string Manufacturer
    # string Name


class Win32_PointingDevice:
""" -> Represents an input device used to point to and select regions on the display of a computer system running Windows."""
    def __init__(self):
    self.Availability = 0
    self.Caption = DEFAULT_STRING_VALUE
    self.Description = DEFAULT_STRING_VALUE
    # datetime InstallDate
    self.Manufacturer = DEFAULT_STRING_VALUE
    self.Name = DEFAULT_STRING_VALUE

    # desc Availability
    # string Caption
    # string Description
    # datetime InstallDate
    # string Manufacturer
    # string Name

class Win32_PhysicalMedia:
""" -> Represents any type of documentation or storage medium."""
    self.Caption = DEFAULT_STRING_VALUE
    self.Description = DEFAULT_STRING_VALUE
    # datetime InstallDate
    self.Name = DEFAULT_STRING_VALUE
    self.Status = DEFAULT_STRING_VALUE
    self.Manufacturer = DEFAULT_STRING_VALUE
    self.Model = DEFAULT_STRING_VALUE
    self.SKU = DEFAULT_STRING_VALUE
    # self.SerialNumber? = None
    self.Tag = None
    self.Version = DEFAULT_STRING_VALUE
    # self.PartNumber? = DEFAULT_STRING_VALUE
    # self.OtherIdentifyingInfo? = DEFAULT_STRING_VALUE
    # boolean PoweredOn
    self.Removable = 0
    self.Replaceable = 0
    # boolean HotSwappable
    self.Capacity = 0
    # desc MediaType
    # string MediaDescription
    # boolean WriteProtectOn
    # boolean CleanerMedia


    # string Caption
    # string Description
    # datetime InstallDate
    # string Name
    # string Status
    # string Manufacturer
    # string Model
    # string SKU
    # string SerialNumber? = NULL
    # string Tag = NULL
    # string Version
    # string PartNumber
    # string OtherIdentifyingInfo
    # boolean PoweredOn
    # boolean Removable
    # boolean Replaceable
    # boolean HotSwappable
    # uint64 Capacity
    # uint16 MediaType
    # string MediaDescription
    # boolean WriteProtectOn
    # boolean CleanerMedia

class Win32_BaseBoard: 
    """-> Represents a baseboard (also known as a motherboard or system board)."""
    self.Caption = DEFAULT_STRING_VALUE
    # string ConfigOptions
    self.Depth = 0.0
    self.Description = DEFAULT_STRING_VALUE
    self.Height = 0.0
    # boolean HostingBoard
    # boolean HotSwappable
    # datetime InstallDate
    self.Manufacturer = DEFAULT_STRING_VALUE
    self.Model = DEFAULT_STRING_VALUE
    self.Name = DEFAULT_STRING_VALUE
    # string OtherIdentifyingInfo
    # string PartNumber
    # boolean PoweredOn
    self.Product = DEFAULT_STRING_VALUE
    self.Removable = 0
    self.Replaceable =0
    # string RequirementsDescription
    # boolean RequiresDaughterBoard
    # string SerialNumber
    self.SKU = Description
    string SlotLayout
    boolean SpecialRequirements
    string Status
    string Tag
    string Version
    real32 Weight
    real32 Width
class Win32_BIOS:
 """-> Represents the attributes of the computer system's basic input or output services (BIOS) that are installed on the computer."""
    uint16 BiosCharacteristics
    string BIOSVersion
    string BuildNumber
    string Caption
    string CodeSet
    string CurrentLanguage
    string Description
    string IdentificationCode
    uint16 InstallableLanguages
    datetime InstallDate
    string LanguageEdition
    String ListOfLanguages
    string Manufacturer
    string Name
    string OtherTargetOS
    boolean PrimaryBIOS
    datetime ReleaseDate
    string SerialNumber
    string SMBIOSBIOSVersion
    uint16 SMBIOSMajorVersion
    uint16 SMBIOSMinorVersion
    boolean SMBIOSPresent
    string SoftwareElementID
    uint16 SoftwareElementState
    string Status
    uint16 TargetOperatingSystem
    string Version
class Win32_MemoryDevice: 
    """-> Represents the properties of a computer system's memory device along with its associated mapped addresses."""
    uint16 Access
    uint8 AdditionalErrorData
    uint16 Availability
    uint64 BlockSize
    string Caption
    uint32 ConfigManagerErrorCode
    boolean ConfigManagerUserConfig
    boolean CorrectableError
    string Description
    string DeviceID
    uint64 EndingAddress
    uint16 ErrorAccess
    uint64 ErrorAddress
    boolean ErrorCleared
    uint8 ErrorData
    uint16 ErrorDataOrder
    string ErrorDescription
    uint16 ErrorGranularity
    uint16 ErrorInfo
    string ErrorMethodology
    uint64 ErrorResolution
    datetime ErrorTime
    uint32 ErrorTransferSize
    datetime InstallDate
    uint32 LastErrorCode
    string Name
    uint64 NumberOfBlocks
    string OtherErrorDescription
    string PNPDeviceID
    uint16 PowerManagementCapabilities
    boolean PowerManagementSupported
    string Purpose
    string Status
    uint16 StatusInfo
    boolean SystemLevelAddress
    string SystemName
class Win32_PhysicalMemory: 
    """-> Represents a physical memory device located on a computer as available to the operating system."""
    string BankLabel
    uint64 Capacity
    string Caption
    uint16 DataWidth
    string Description
    string DeviceLocator
    uint16 FormFactor
    boolean HotSwappable
    datetime InstallDate
    uint16 InterleaveDataDepth
    uint32 InterleavePosition
    string Manufacturer
    uint16 MemoryType
    string Model
    string Name
    string OtherIdentifyingInfo
    string PartNumber
    uint32 PositionInRow
    boolean PoweredOn
    boolean Removable
    boolean Replaceable
    string SerialNumber
    string SKU
    uint32 Speed
    string Status
    string Tag
    uint16 TotalWidth
    uint16 TypeDetail
    string Version
class Win32_Processor: 
    """-> Represents a device capable of interpreting a sequence of machine instructions on a computer system running Windows."""
    uint16 AddressWidth
    uint16 Architecture
    uint16 Availability
    string Caption
    uint32 ConfigManagerErrorCode
    boolean ConfigManagerUserConfig
    uint16 CpuStatus
    string CreationClassName
    uint32 CurrentClockSpeed
    uint16 CurrentVoltage
    uint16 DataWidth
    string Description
    string DeviceID
    boolean ErrorCleared
    string ErrorDescription
    uint32 ExtClock
    uint16 Family
    datetime InstallDate
    uint32 L2CacheSize
    uint32 L2CacheSpeed
    uint32 L3CacheSize
    uint32 L3CacheSpeed
    uint32 LastErrorCode
    uint16 Level
    uint16 LoadPercentage
    string Manufacturer
    uint32 MaxClockSpeed
    string Name
    uint32 NumberOfCores
    uint32 NumberOfLogicalProcessors
    string OtherFamilyDescription
    string PNPDeviceID
    uint16 PowerManagementCapabilities
    boolean PowerManagementSupported
    string ProcessorId
    uint16 ProcessorType
    uint16 Revision
    string Role
    string SocketDesignation
    string Status
    uint16 StatusInfo
    string Stepping
    string SystemCreationClassName
    string SystemName
    string UniqueId
    uint16 UpgradeMethod
    string Version
    uint32 VoltageCaps
class Win32_Printer: 
    """-> Represents a device connected to a computer system running Windows that is capable of reproducing a visual image on a medium."""
    uint32 Attributes
    uint16 Availability
    string Caption
    string CharSetsSupported
    string Comment
    uint32 ConfigManagerErrorCode
    boolean ConfigManagerUserConfig
    string CurrentCharSet
    uint16 CurrentLanguage
    string CurrentMimeType
    string CurrentPaperType
    boolean Default
    uint32 DefaultCopies
    uint16 DefaultLanguage
    string DefaultMimeType
    uint32 DefaultNumberUp
    string DefaultPaperType
    uint32 DefaultPriority
    string Description
    uint16 DetectedErrorState
    string DeviceID
    boolean Direct
    string DriverName
    boolean ErrorCleared
    string ErrorDescription
    string ErrorInformation
    uint16 ExtendedDetectedErrorState
    uint16 ExtendedPrinterStatus
    uint32 HorizontalResolution
    datetime InstallDate
    uint32 JobCountSinceLastReset
    boolean KeepPrintedJobs
    uint16 LanguagesSupported
    uint32 LastErrorCode
    boolean Local
    string Location
    uint16 MarkingTechnology
    uint32 MaxCopies
    uint32 MaxNumberUp
    uint32 MaxSizeSupported
    string MimeTypesSupported
    string Name
    boolean Network
    uint16 PaperSizesSupported
    string PaperTypesAvailable
    string Parameters
    string PNPDeviceID
    string PortName
    uint32 PrinterState
    uint16 PrinterStatus
    string PrintJobDataType
    string PrintProcessor
    uint32 Priority
    boolean Published
    boolean Queued
    string SeparatorFile
    string ServerName
    boolean Shared
    string ShareName
    boolean SpoolEnabled
    datetime StartTime
    string Status
    uint16 StatusInfo
    string SystemName
    datetime TimeOfLastReset
    datetime UntilTime
    uint32 VerticalResolution
    boolean WorkOffline
class Win32_DesktopMonitor: 
    """-> Represents the type of monitor or display device attached to the computer system."""
    uint16 Availability
    uint32 Bandwidth
    string Caption
    uint32 ConfigManagerErrorCode
    boolean ConfigManagerUserConfig
    string Description
    string DeviceID
    uint16 DisplayType
    boolean ErrorCleared
    string ErrorDescription
    datetime InstallDate
    uint32 LastErrorCode
    string MonitorManufacturer
    string MonitorType
    string Name
    uint32 PixelsPerXLogicalInch
    uint32 PixelsPerYLogicalInch
    string PNPDeviceID
    uint32 ScreenHeight
    uint32 ScreenWidth
    string Status
    uint16 StatusInfo
    string SystemName
        

class OutputMaker(Computador):
    """Classe OutputMaker, cria a saída do agente."""

    def __init__(self):
        self.output = ""
        self.placaRede = Rede()
        # computador = Computador()
        # computador.coletar()

    def getWin32_Keyboard:
     """-> Represents a keyboard installed on a computer system running Windows."""
        desc = "[Availability][/Availability]"
        desc += "[Caption][/Caption]"
        desc += "[Description][/Description]"
        desc += "[InstallDate][/InstallDate]"
        desc += "[Manufacturer][/Manufacturer]"
        desc += "[Name][/Name]"
        return desc

    def getWin32_PointingDevice:
    """ -> Represents an input device used to point to and select regions on the display of a computer system running Windows."""
        desc = "[Availability][/Availability]"
        desc += "[Caption][/Caption]"
        desc += "[Description][/Description]"
        desc += "[InstallDate][/InstallDate]"
        desc += "[Manufacturer][/Manufacturer]"
        desc += "[Name][/Name]"
        return desc

    def getWin32_PhysicalMedia:
    """ -> Represents any type of documentation or storage medium."""
        desc = "[Caption][/Caption]"
        desc += "[Description][/Description]"
        desc += "[InstallDate][/InstallDate]"
        desc += "[Name][/Name]"
        desc += "[Status][/Status]"
        desc += "[Manufacturer][/Manufacturer]"
        desc += "[Model][/Model]"
        desc += "[SKU][/SKU]"
        desc += "[SerialNumber]%s[/SerialNumber]" % None
        desc += "[Tag]%s[/Tag]" % None
        desc += "[Version][/Version]"
        desc += "[PartNumber][/PartNumber]"
        desc += "[OtherIdentifyingInfo][/OtherIdentifyingInfo]"
        desc += "[PoweredOn][/PoweredOn]"
        desc += "[Removable][/Removable]"
        desc += "[Replaceable][/Replaceable]"
        desc += "[HotSwappable][/HotSwappable]"
        desc += "[Capacity][/Capacity]"
        desc += "[MediaType][/MediaType]"
        desc += "[MediaDescription]/[MediaDescription]"
        desc += "[WriteProtectOn][/WriteProtectOn]"
        desc += "[CleanerMedia][/CleanerMedia]"

    def getWin32_BaseBoard:
    """ -> Represents a baseboard (also known as a motherboard or system board)."""
        desc = "[Caption][/Caption]"
        desc += "[ConfigOptions][/ConfigOptions]"
        desc += "[Depth][/Depth]"
        desc += "[Description][/Description]"
        desc += "[Height][/Height]"
        desc += "[HostingBoard][/HostingBoard]"
        desc += "[HotSwappable][/HotSwappable]"
        desc += "[InstallDate][/InstallDate"
        desc += "[Manufacturer][/Manufacturer]"
        desc += "[Model][/Model]"
        desc += "[Name][/Name]"
        desc += "[OtherIdentifyingInfo][/OtherIdentifyingInfo]"
        desc += "[PartNumber][/PartNumber]"
        desc += "[PoweredOn][/PoweredOn]"
        desc += "[Product][/Product]"
        desc += "[Removable][/Removable]"
        desc += "[Replaceable][/Replaceable]"
        desc += "[RequirementsDescription][/RequirementsDescription]"
        desc += "[RequiresDaughterBoard][/RequiresDaughterBoard]"
        desc += "[SerialNumber][/SerialNumber]"
        desc += "[SKU][/SKU]"
        desc += "[SlotLayout][/SlotLayout]"
        desc += "[SpecialRequirements][/SpecialRequirements]"
        desc += "[Status][/Status]"
        desc += "[Tag][/Tag]"
        desc += "[Version][/Version]"
        desc += "[Weight][/Weight]"
        desc += "[Width][/Width]"
        return desc

    def getWin32_BIOS:
    """ -> Represents the attributes of the computer system's basic input or output services (BIOS) that are installed on the computer."""
        desc = "[BiosCharacteristics][/BiosCharacteristics]"
        desc += "[BIOSVersion][/BIOSVersion]"
        desc += "[BuildNumber][/BuildNumber]"
        desc += "[Caption][/Caption]"
        desc += "[CodeSet][/CodeSet]"
        desc += "[CurrentLanguage][/CurrentLanguage]"
        desc += "[Description][/Description]"
        desc += "[IdentificationCode][/IdentificationCode]"
        desc += "[InstallableLanguages][/InstallableLanguages]"
        desc += "[InstallDate][/InstallDate]"
        desc += "[LanguageEdition][/LanguageEdition]"
        desc += "[ListOfLanguages][/ListOfLanguages]"
        desc += "[Manufacturer][/Manufacturer]"
        desc += "[Name][/Name]"
        desc += "[OtherTargetOS][/OtherTargetOS]"
        desc += "[PrimaryBIOS][/PrimaryBIOS]"
        desc += "[ReleaseDate][/ReleaseDate]"
        desc += "[SerialNumber][/SerialNumber]"
        desc += "[SMBIOSBIOSVersion][/SMBIOSBIOSVersion]"
        desc += "[SMBIOSMajorVersion][/SMBIOSMajorVersion]"
        desc += "[SMBIOSMinorVersion][/SMBIOSMinorVersion]"
        desc += "[SMBIOSPresent][/SMBIOSPresent]"
        desc += "[SoftwareElementID][/SoftwareElementID]"
        desc += "[SoftwareElementState][/SoftwareElementState]"
        desc += "[Status][/Status]"
        desc += "[TargetOperatingSystem][/TargetOperatingSystem]"
        desc += "[Version][/Version]"
        return desc
 
    def getWin32_MemoryDevice:
    """ -> Represents the properties of a computer system's memory device along with its associated mapped addresses."""
        desc = "[Access][/Access]"
        desc += "[AdditionalErrorData][/AdditionalErrorData]"
        desc += "[Availability][/Availability]"
        desc += "[BlockSize][/BlockSize]"
        desc += "[Caption][/Caption]"
        desc += "[ConfigManagerErrorCode][/ConfigManagerErrorCode]"
        desc += "[ConfigManagerUserConfig][/ConfigManagerUserConfig]"
        desc += "[CorrectableError][/CorrectableError]"
        desc += "[Description][/Description]"
        desc += "[DeviceID][/DeviceID]"
        desc += "[EndingAddress][/EndingAddress]"
        desc += "[ErrorAccess][/ErrorAccess]"
        desc += "[ErrorAddress][/ErrorAddress]"
        desc += "[ErrorCleared][/ErrorCleared]"
        desc += "[ErrorData][/ErrorData]"
        desc += "[ErrorDataOrder][/ErrorDataOrder]"
        desc += "[ErrorDescription][/ErrorDescription]"
        desc += "[ErrorGranularity][/ErrorGranularity]"
        desc += "[ErrorInfo][/ErrorInfo]"
        desc += "[ErrorMethodology][/ErrorMethodology]"
        desc += "[ErrorResolution][/ErrorResolution]"
        desc += "[ErrorTime][/ErrorTime]"
        desc += "[ErrorTransferSize][/ErrorTransferSize]"
        desc += "[InstallDate][/InstallDate]"
        desc += "[LastErrorCode][/LastErrorCode]"
        desc += "[Name][/Name]"
        desc += "[NumberOfBlocks][/NumberOfBlocks]"
        desc += "[OtherErrorDescription][/OtherErrorDescription]"
        desc += "[PNPDeviceID][/PNPDeviceID]"
        desc += "[PowerManagementCapabilities][/PowerManagementCapabilities]"
        desc += "[PowerManagementSupported][/PowerManagementSupported]"
        desc += "[Purpose][/Purpose]"
        desc += "[Status][/Status]"
        desc += "[StatusInfo][/StatusInfo]"
        desc += "[SystemLevelAddress][/SystemLevelAddress]"
        desc += "[SystemName][/SystemName]"
        return desc

    def getWin32_PhysicalMemory:
    """ -> Represents a physical memory device located on a computer as available to the operating system."""
        desc = "[BankLabel][/BankLabel]"
        desc += "[Capacity][/Capacity]"
        desc += "[Caption][/Caption]"
        desc += "[DataWidth][/DataWidth]"
        desc += "[Description][/Description]"
        desc += "[DeviceLocator][/DeviceLocator]"
        desc += "[FormFactor][/FormFactor]"
        desc += "[HotSwappable][/HotSwappable]"
        desc += "[InstallDate][/InstallDate]"
        desc += "[InterleaveDataDepth][/InterleaveDataDepth]"
        desc += "[InterleavePosition][/InterleavePosition]"
        desc += "[Manufacturer][/Manufacturer]"
        desc += "[MemoryType][/MemoryType]"
        desc += "[Model][/Model]"
        desc += "[Name][/Name]"
        desc += "[OtherIdentifyingInfo][/OtherIdentifyingInfo]"
        desc += "[PartNumber][/PartNumber]"
        desc += "[PositionInRow][/PositionInRow]"
        desc += "[PoweredOn][/PoweredOn]"
        desc += "[Removable][/Removable]"
        desc += "[Replaceable][/Replaceable]"
        desc += "[SerialNumber][/SerialNumber]"
        desc += "[SKU][/SKU]"
        desc += "[Speed][/Speed]"
        desc += "[Status][/Status]"
        desc += "[Tag][/Tag]"
        desc += "[TotalWidth][/TotalWidth]"
        desc += "[TypeDetail][/TypeDetail]"
        desc += "[Version][/Version]"

    def getWin32_Processor:
    """ -> Represents a device capable of interpreting a sequence of machine instructions on a computer system running Windows."""
        desc = "[AddressWidth][/AddressWidth]"
        desc += "[Architecture][/Architecture]"
        desc += "[Availability][/Availability]"
        desc += "[Caption][/Caption]"
        desc += "[ConfigManagerErrorCode][/ConfigManagerErrorCode]"
        desc += "[ConfigManagerUserConfig][/ConfigManagerUserConfig]"
        desc += "[CpuStatus][/CpuStatus]"
        desc += "[CreationClassName][/CreationClassName]"
        desc += "[CurrentClockSpeed][/CurrentClockSpeed]"
        desc += "[CurrentVoltage][/CurrentVoltage]"
        desc += "[DataWidth][/DataWidth]"
        desc += "[Description][/Description]"
        desc += "[DeviceID][/DeviceID]"
        desc += "[ErrorCleared][/ErrorCleared]"
        desc += "[ErrorDescription][/ErrorDescription]"
        desc += "[ExtClock][/ExtClock]"
        desc += "[Family][/Family]"
        desc += "[InstallDate][/InstallDate]"
        desc += "[L2CacheSize][/L2CacheSize]"
        desc += "[L2CacheSpeed][/L2CacheSpeed]"
        desc += "[L3CacheSize][/L3CacheSize]"
        desc += "[L3CacheSpeed][/L3CacheSpeed]"
        desc += "[LastErrorCode][/LastErrorCode]"
        desc += "[Level][/Level]"
        desc += "[LoadPercentage][/LoadPercentage]"
        desc += "[Manufacturer][/Manufacturer]"
        desc += "[MaxClockSpeed][/MaxClockSpeed]"
        desc += "[Name][/Name]"
        desc += "[NumberOfCores][/NumberOfCores]"
        desc += "[NumberOfLogicalProcessors][/NumberOfLogicalProcessors]"
        desc += "[OtherFamilyDescription][/OtherFamilyDescription]"
        desc += "[PNPDeviceID][/PNPDeviceID]"
        desc += "[PowerManagementCapabilities][/PowerManagementCapabilities]"
        desc += "[PowerManagementSupported][/PowerManagementSupported]"
        desc += "[ProcessorId][/ProcessorId]"
        desc += "[ProcessorType][/ProcessorType]"
        desc += "[Revision][/Revision]"
        desc += "[Role][/Role]"
        desc += "[SocketDesignation][/SocketDesignation]"
        desc += "[Status][/Status]"
        desc += "[StatusInfo][/StatusInfo]"
        desc += "[Stepping][/Stepping]"
        desc += "[SystemCreationClassName][/SystemCreationClassName]"
        desc += "[SystemName][/SystemName]"
        desc += "[UniqueId][/UniqueId]"
        desc += "[UpgradeMethod][/UpgradeMethod]"
        desc += "[Version][/Version]"
        desc += "[VoltageCaps][/VoltageCaps]"
        return desc

    def getWin32_Printer:
    """ -> Represents a device connected to a computer system running Windows that is capable of reproducing a visual image on a medium."""
        desc = "[Attributes][/Attributes]"
        desc += "[Availability][/Availability]"
        desc += "[Caption][/Caption]"
        desc += "[CharSetsSupported][/CharSetsSupported]"
        desc += "[Comment][/Comment]"
        desc += "[ConfigManagerErrorCode][/ConfigManagerErrorCode]"
        desc += "[ConfigManagerUserConfig][/ConfigManagerUserConfig]"
        desc += "[CurrentCharSet][/CurrentCharSet]"
        desc += "[CurrentLanguage][/CurrentLanguage]"
        desc += "[CurrentMimeType][/CurrentMimeType]"
        desc += "[CurrentPaperType][/CurrentPaperType]"
        desc += "[Default][/Default]"
        desc += "[DefaultCopies][/DefaultCopies]"
        desc += "[DefaultLanguage][/DefaultLanguage]"
        desc += "[DefaultMimeType][/DefaultMimeType]"
        desc += "[DefaultNumberUp][/DefaultNumberUp]"
        desc += "[DefaultPaperType][/DefaultPaperType]"
        desc += "[DefaultPriority][/DefaultPriority]"
        desc += "[Description][/Description]"
        desc += "[DetectedErrorState][/DetectedErrorState]"
        desc += "[DeviceID][/DeviceID]"
        desc += "[Direct][/Direct]"
        desc += "[DriverName][/DriverName]"
        desc += "[ErrorCleared][/ErrorCleared]"
        desc += "[ErrorDescription][/ErrorDescription]"
        desc += "[ErrorInformation][/ErrorInformation]"
        desc += "[ExtendedDetectedErrorState][/ExtendedDetectedErrorState]"
        desc += "[ExtendedPrinterStatus][/ExtendedPrinterStatus]"
        desc += "[HorizontalResolution][/HorizontalResolution]"
        desc += "[InstallDate][/InstallDate]"
        desc += "[JobCountSinceLastReset][/JobCountSinceLastReset]"
        desc += "[KeepPrintedJobs][/KeepPrintedJobs]"
        desc += "[LanguagesSupported][/LanguagesSupported]"
        desc += "[LastErrorCode][/LastErrorCode]"
        desc += "[Local][/Local]"
        desc += "[Location][/Location]"
        desc += "[MarkingTechnology][/MarkingTechnology]"
        desc += "[MaxCopies][/MaxCopies]"
        desc += "[MaxNumberUp][/MaxNumberUp]"
        desc += "[MaxSizeSupported][/MaxSizeSupported]"
        desc += "[MimeTypesSupported][/MimeTypesSupported]"
        desc += "[Name][/Name]"
        desc += "[Network][/Network]"
        desc += "[PaperSizesSupported][/PaperSizesSupported]"
        desc += "[PaperTypesAvailable][/PaperTypesAvailable]"
        desc += "[Parameters][/Parameters]"
        desc += "[PNPDeviceID][/PNPDeviceID]"
        desc += "[PortName][/PortName]"
        desc += "[PrinterState][/PrinterState]"
        desc += "[PrinterStatus][/PrinterStatus]"
        desc += "[PrintJobDataType][/PrintJobDataType]"
        desc += "[PrintProcessor][/PrintProcessor]"
        desc += "[Priority][/Priority]"
        desc += "[Published][/Published]"
        desc += "[Queued][/Queued]"
        desc += "[SeparatorFile][/SeparatorFile]"
        desc += "[ServerName][/ServerName]"
        desc += "[Shared][/Shared]"
        desc += "[ShareName][/ShareName]"
        desc += "[SpoolEnabled][/SpoolEnabled]"
        desc += "[StartTime][/StartTime]"
        desc += "[Status][/Status]"
        desc += "[StatusInfo][/StatusInfo]"
        desc += "[SystemName][/SystemName]"
        desc += "[TimeOfLastReset][/TimeOfLastReset]"
        desc += "[UntilTime][/UntilTime]"
        desc += "[VerticalResolution][/VerticalResolution]"
        desc += "[WorkOffline][/WorkOffline]"
        return desc

    def getWin32_DesktopMonitor:
    """ -> Represents the type of monitor or display device attached to the computer system."""
        desc = "[Availability][/Availability]"
        desc += "[Bandwidth][/Bandwidth]"
        desc += "[Caption][/Caption]"
        desc += "[ConfigManagerErrorCode][/ConfigManagerErrorCode]"
        desc += "[ConfigManagerUserConfig][/ConfigManagerUserConfig]"
        desc += "[Description][/Description]"
        desc += "[DeviceID][/DeviceID]"
        desc += "[DisplayType][/DisplayType]"
        desc += "[ErrorCleared][/ErrorCleared]"
        desc += "[ErrorDescription][/ErrorDescription]"
        desc += "[InstallDate][/InstallDate]"
        desc += "[LastErrorCode][/LastErrorCode]"
        desc += "[MonitorManufacturer][/MonitorManufacturer]"
        desc += "[MonitorType][/MonitorType]"
        desc += "[Name][/Name]"
        desc += "[PixelsPerXLogicalInch][/PixelsPerXLogicalInch]"
        desc += "[PixelsPerYLogicalInch][/PixelsPerYLogicalInch]"
        desc += "[PNPDeviceID][/PNPDeviceID]"
        desc += "[ScreenHeight][/ScreenHeight]"
        desc += "[ScreenWidth][/ScreenWidth]"
        desc += "[Status][/Status]"
        desc += "[StatusInfo][/StatusInfo]"
        desc += "[SystemName][/SystemName]"
        return desc

    def getOS:
        """Metodo getOS da Classe"""
        # Sistema operacional
        # [Caption]Microsoft Windows 7 Home Basic[/Caption][CSDVersion]Service Pack 1[/CSDVersion][InstallDate]20111202184401.000000-120[/InstallDate][LastBootUpTime]20130910092553.109999-180[/LastBootUpTime][NumberOfLicensedUsers]0[/NumberOfLicensedUsers][OSArchitecture]64-bit[/OSArchitecture][OSLanguage]1046[/OSLanguage][ProductType]1[/ProductType][SerialNumber]00346-OEM-8992752-50066[/SerialNumber][Version]6.1.7601[/Version]
        desc = "[Caption]%s[/Caption]" % self.getSO()
        desc += "[CSDVersion][/CSDVersion]"
        desc += "[InstallDate][/InstallDate]"
        desc += "[LastBootUpTime][/LastBootUpTime]"
        desc += "[NumberOfLicensedUsers][/NumberOfLicensedUsers]"
        desc += "[OSArchitecture][/OSArchitecture]"
        desc += "[OSLanguage][/OSLanguage]"
        desc += "[ProductType][/ProductType]"
        desc += "[SerialNumber][/SerialNumber]"
        desc += "[Version][/Version]"
        return desc

    def getCompSys:
        # Computer System

        # # A coleta ComputerSystem deve possuir as seguintes informações:
        desc = "[Caption][/Caption]"
        desc += "[Domain][/Domain]"
        desc += "[TotalPhysicalMemory][/TotalPhysicalMemory]"
        desc += "[UserName][/UserName]"
        return desc
        # [Caption]EDUARDO-MEGA[/Caption][Domain]WORKGROUP[/Domain][TotalPhysicalMemory]6229110784[/TotalPhysicalMemory][UserName]eduardo-mega\\edu
        # ardo[/UserName]
        # Network Adapter Interface
    
    def getRede:
        # A coleta NetworkAdapterInterface deve fornecer as seguintes informações:
        for pr in self.placaRede:
            desc = "[DefaultIPGateway]%s[/DefaultIPGateway]" % pr.getGateway
            desc += "[Description]%s[/Description]" % pr.getDescricao
            desc += "[DHCPServer]%s[/DHCPServer]" % pr.getDHCP
            desc += "[DNSDomain]%s[/DNSDomain]" % pr.getDNSDomain
            desc += "[DNSHostName]%s[/DNSHostName]" % pr.getLogicalName
            desc += "[DNSServerSearchOrder]%s[/DNSServerSearchOrder]" % pr.getDNS
            desc += "[IPAddress]%s[/IPAddress]" % pr.getIP
            desc += "[IPSubnet]%s[/IPSubnet]" % pr.getIPRede
            desc += "[MACAddress]%s[/MACAddress]" % pr.getMAC
            desc += "[WINSPrimaryServer][/WINSPrimaryServer]"
            desc += "[WINSSecondaryServer][/WINSSecondaryServer]"
            return desc


        # [DefaultIPGateway]192.168.25.1[/DefaultIPGateway][Description]JMicron PCI Express Gigabit Ethernet Adapter[/Description][DHC
        # PServer]192.168.25.1[/DHCPServer][DNSDomain]home[/DNSDomain][DNSHostName]eduardo-mega[/DNSHostName][DNSServerSearchOrder]192.168.25.1[/DNSServerSearch
        # Order][IPAddress]192.168.25.14[/IPAddress][IPSubnet]255.255.255.0[/IPSubnet][MACAddress]00:90:F5:95:39:42[/MACAddress][WINSPrimaryServer][/WINSPrimary
        # Server][WINSSecondaryServer][/WINSSecondaryServer]


    def getSoft:
        # A coleta SoftwareList deve fornecer as seguintes informações:

        # [Software][IDSoftware]AddressBook[/IDSoftware][DisplayName][/DisplayName][DisplayVersion][/DisplayVersion][URLInfoAbout][/URLInfoAbout][Pub
        # lisher][/Publisher][/Software][Software][IDSoftware]Adobe AIR[/IDSoftware][DisplayName]Adobe AIR[/DisplayName][DisplayVersion]2.6.0.19140[/DisplayVers
        # ion][URLInfoAbout][/URLInfoAbout][Publisher]Adobe Systems Incorporated[/Publisher][/Software][Software][IDSoftware]AMCap[/IDSoftware][DisplayName]AMCa
        # p[/DisplayName][DisplayVersion]9.20.132.2[/DisplayVersion][URLInfoAbout]http://noeld.com/[/URLInfoAbout][Publisher]No\xebl Danjou[/Publisher][/Softwar
        # e][Software][IDSoftware]avast[/IDSoftware][DisplayName]avast! Free Antivirus[/DisplayName][DisplayVersion]8.0.1489.0[/DisplayVersion][URLInfoAbout][/U
        # RLInfoAbout][Publisher]AVAST Software[/Publisher][/Software]

        for prog in SoftwareList
            desc = "[Software]"
            desc += "[IDSoftware][/IDSoftware]"
            desc += "[DisplayName][/DisplayName]"
            desc += "[DisplayVersion][/DisplayVersion]"
            desc += "[URLInfoAbout][/URLInfoAbout]"
            desc += "[Publisher][/Publisher]"
            desc += "[/Software]"
        return desc

        # Cada software é delimitado pela tag [Software][/Software], sendo que cada um possui os seguintes atributos:

        #     [IDSoftware]Identificador único do Software, que pode ser uma desc[/IDSoftware]. Ex.: [IDSoftware]libreoffice[/IDSoftware]
        #     [DisplayName]Nome do Software[/DisplayName]
        #     [DisplayVersion]Versão[/DisplayVersion]
        #     [URLInfoAbout]Se existir, página do software[/URLInfoAbout]
        #     [Publisher]Quem é o fabricante[/Publisher]

        desc = "Computador \n"
        desc += "\tSistema Operacional: %s \n" % self.getSO()
        desc += "\tHostname: %s \n" % self.getHostName()
        desc += "Placa Mae \n"
        desc += "\tDescricao: %s \n" % self.getPlacaMae()
        desc += "Bios \n"
        desc += "\tDescricao: %s \n" % self.bios.getDescricao()
        desc += "\tData: %s \n" % self.bios.getData()
        for c in self.cpu:
            desc += "CPU \n"
            desc += "\tId: %s \n" % c.getId()
            desc += "\tFrequencia: %s \n" % c.getFrequencia()
            desc += "\tDescricao: %s \n" % c.getDescricao()
            desc += "\tSerial: %s \n" % c.getSerial()
        for hd in self.hardDisk:
            desc += "HD \n"
            desc += "\tTamanho: %s Mb \n" % hd.getTamanho()
            desc += "\tDescricao: %s \n" % hd.getDescricao()
            desc += "\tFabricante: %s \n" % hd.getFabricante()
        desc += "Teclado \n"
        desc += "\tDescricao: %s \n" % self.getTeclado()
        desc += "Mouse \n"
        desc += "\tDescricao: %s \n" % self.getMouse()
        for v in self.video:
            desc += "Video \n"
            desc += "\tRam: %s Mb \n" % v.getRam()
            desc += "\tCores: %s \n" % v.getCores()
            desc += "\tDescricao: %s \n" % v.getDescricao()
        for a in self.audio:
            desc += "Audio \n"
            desc += "\tDescricao: %s \n" % a
        for m in self.modem:
            desc += "Modem \n"
            desc += "\tDescricao: %s \n" % m
        desc += "Ram \n"
        desc += "\tTamanho: %s Mb \n" % self.ram.getTamanho()
        desc += "\tDescricao: %s \n" % self.ram.getDescricao()
        for r in self.rom:
            desc += "Rom \n"
            desc += "\tDescricao: %s \n" % r
        for pr in self.placaRede:
            desc += "Placa de Rede \n"
            desc += "\tFabricante: %s \n" % pr.getFabricante()
            desc += "\tDescricao: %s \n" % pr.getDescricao()
            desc += "\tEndereco IP: %s \n" % pr.getIP()
            desc += "\tMascara de Rede: %s \n" % pr.getMascara()
            desc += "\tEndereco Mac: %s \n" % pr.getMAC()
            desc += "\tLogicalname Mac: %s \n" % pr.getLogicalName()
        return desc 

