from steam.enums import EResult
from steam.core.msg import MsgProto
from steam.enums.emsg import EMsg
from steam.client import SteamClient

message = MsgProto(EMsg.ClientPersonaState)
print(message.parse())
#message.body.steamid_to_add = 76561198044525640

client = SteamClient()
r = client.login(username='antenka33',password='vlodos33')

resp = client.send_message_and_wait(message, EMsg.ClientPersonaState)

print(message.body)
print(message.msg)

if resp.eresult == EResult.OK:
	print(resp)
    #print ("Send a friend request to %s (%d)".format(resp.body.persona_name_added,
                                               #resp.body.steam_id_added))
                                               
else:
    print (EResult(resp.eresult))