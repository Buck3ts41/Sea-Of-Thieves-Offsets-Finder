"""
Script that is responsible for looking through our SDK and determining
all of the offsets we specify automatically. Can that pass the output file
into the SoT ESP Framework
@Author https://github.com/DougTheDruid
@Modified by https://github.com/Buck3ts41
"""
import json


ATHENA = "SDKs\\JSON-SDK\\Athena_Classes.json"
ENGINE = "SDKs\\JSON-SDK\\Engine_Classes.json"
ATHENA_AI = "SDKs\\JSON-SDK\\AthenaAI_Classes.json"
ENGINE_STRUCT = "SDKs\\JSON-SDK\\Engine_Structs.json"
ATHENA_STRUCT = "SDKs\\JSON-SDK\\Athena_structs.json"


def get_offset(file_name, title, memory_object):
    """
    Opens the file the offset lives within, then reads through the lines within
    the file until we find the offset in hex.
    :param file_name: The file name where the offset lives within
    :param title: The title of the primary object which contains the value we
    want to pull data from
    :param memory_object: The data name from a parent object we want to pull
    the offset from
    :return: The int-converted version of the offset for a specific data field
    out of a parent object
    """
    offset = "Not Found"
    with open(file_name) as file_to_check:
        json_sdk_file = json.load(file_to_check)
        components = json_sdk_file.get(title, None)
        if components:
            attributes = components.get('Attributes', None)
            for attribute in attributes:
                if attribute['Name'] == memory_object:
                    offset = int(attribute.get('Offset'), 16)
    return offset


def get_size(file_name, title):
    """
    Determines the size of a struct or class given a specific file to look in
    :param file_name: The file name where the class or struct lives
    :param title: The class or struct name we want the size of
    :return: The int-converted version of the size for a class or struct
    """
    offset = "Not Found"
    with open(file_name) as file_to_check:
        json_sdk_file = json.load(file_to_check)
        components = json_sdk_file.get(title, None)
        if components:
            return int(components.get('ClassSize'), 16)
    return offset


if __name__ == '__main__':
    """
    We build a dictionary which contains all offset data, then save the 
    information into an offset file.
    """

    output = {
        "Actor.actorId": 24,
        "SceneComponent.ActorCoordinates": 0x12c,
        "Actor.rootComponent": get_offset(ENGINE, "Actor", "RootComponent"),
        "CameraCacheEntry.MinimalViewInfo": get_offset(ENGINE_STRUCT, "CameraCacheEntry", "POV"),
        "Crew.Size": get_size(ATHENA_STRUCT, "Crew"),
        "Crew.Players": get_offset(ATHENA_STRUCT, "Crew", "Players"),
        "GameInstance.LocalPlayers": get_offset(ENGINE, "GameInstance", "LocalPlayers"),
        "LocalPlayer.PlayerController": get_offset(ENGINE, "Player", "PlayerController"),
        "PlayerCameraManager.CameraCache": get_offset(ENGINE, "PlayerCameraManager", "CameraCache"),
        "PlayerController.CameraManager": get_offset(ENGINE, "PlayerController", "PlayerCameraManager"),
        "PlayerState.PlayerName": get_offset(ENGINE, "PlayerState", "PlayerName"),
        "World.OwningGameInstance": get_offset(ENGINE, "World", "OwningGameInstance"),
        "World.PersistentLevel": get_offset(ENGINE, "World", "PersistentLevel"),
	"APlayerController.Pawn" : get_offset(ENGINE, "Controller", "Pawn"),
	"APlayerController.Character" : get_offset(ENGINE, "Controller", "Character"),
	"APlayerController.CameraManager" : get_offset(ENGINE, "PlayerController", "CameraManager"),
	"APlayerController.ControlRotation" : get_offset(ENGINE, "PlayerController", "ControlRotation"),
        "AActor.PlayerState" : get_offset(ENGINE, "Pawn", "PlayerState"),
        "AActor.WieldedItemComponent" : get_offset(ATHENA, "AthenaCharacter", "WieldedItemComponent"),
        "AActor.HealthComponent" : get_offset(ATHENA, "AthenaCharacter", "HealthComponent"),
        "AActor.DrowningComponent" : get_offset(ATHENA, "AthenaPlayerCharacter", "DrowningComponent"),
        "AItemProxy.AItemInfo" : get_offset(ATHENA, "ItemProxy", "ItemInfo"),
        "AItemInfo.UItemDesc" : get_offset(ATHENA, "ItemInfo", "Desc"),
        "ABootyItemInfo.BootyType" : get_offset(ATHENA, "BootyItemInfo", "BootyType"),
        "ABootyItemInfo.Rarity" : get_offset(ATHENA, "BootyItemInfo", "Rarity"),
        "AShip.CrewOwnershipComponent" : get_offset(ATHENA, "Ship", "CrewOwnershipComponent"),
        "AShip.ShipInternalWaterComponent" : get_offset(ATHENA, "Ship", "ShipInternalWaterComponent"),
        "AShip.ShipOwningActor" : get_offset(ATHENA, "HullDamage", "Root"),
        "UCrewOwnershipComponent.CrewId" : get_offset(ATHENA, "CrewOwnershipComponent", "CachedCrewId"),
        "ACrewService.Crews" : get_offset(ATHENA, "CrewService", "Crews"),
        "AFauna.Name" : get_offset(ATHENA_AI, "Fauna", "DisplayName"),
        "AMapTable.MapPins" : get_offset(ATHENA, "MapTable", "MapPins"),
        "AMapTable.ServerCenter" : get_offset(ATHENA, "MapTable", "ServerCentreLocation"),
        "AMapTable.TrackedShips" : get_offset(ATHENA, "MapTable", "TrackedShips"),
        "UWieldedItemComponent.WieldedItem" : get_offset(ATHENA, "WieldedItemComponent", "WieldedItem"),
        "AWieldableItem.ItemInfo" : get_offset(ATHENA, "WieldableItem", "ItemInfo"),
        "ACannon.TimePerFire" : get_offset(ATHENA, "Cannon", "TimePerFire"),
        "ACannon.ProjectileSpeed" : get_offset(ATHENA, "Cannon", "ProjectileSpeed"),
        "ACannon.ProjectileGravityScale" : get_offset(ATHENA, "Cannon", "ProjectileGravityScale"),
        "ACannon.ServerPitch" : get_offset(ATHENA, "Cannon", "ServerPitch"),

    }
    with open("offsets.json", "w+") as outfile:
        outfile.write(json.dumps(output, indent=2, sort_keys=True))
