import ns.core
import ns.network
import ns.internet
import ns.mobility
import ns.wifi
import ns.applications

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Generate RSA keys for vehicles (simulate trusted setup)
key1 = RSA.generate(2048)
pub_key1 = key1.publickey()

def sign_message(private_key, message):
    h = SHA256.new(message)
    signature = pkcs1_15.new(private_key).sign(h)
    return signature

def verify_signature(public_key, message, signature):
    h = SHA256.new(message)
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False

def secure_send(source_id, message):
    # Each node signs the message before sending
    signature = sign_message(key1, message)
    return message, signature

def secure_receive(dest_id, message, signature):
    # Node verifies the received message
    return verify_signature(pub_key1, message, signature)

# Network Configuration
nodes = ns.network.NodeContainer()
nodes.Create(3)

wifi_helper = ns.wifi.WifiHelper.Default()
phy = ns.wifi.YansWifiPhyHelper.Default()
channel = ns.wifi.YansWifiChannelHelper.Default().Create()
phy.SetChannel(channel)

mac = ns.wifi.WifiMacHelper()
mac.SetType("ns3::AdhocWifiMac")

devices = wifi_helper.Install(phy, mac, nodes)

mobility = ns.mobility.MobilityHelper()
mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel")
mobility.Install(nodes)

stack = ns.internet.InternetStackHelper()
stack.Install(nodes)

address = ns.internet.Ipv4AddressHelper()
address.SetBase(ns.network.Ipv4Address("10.0.0.0"), ns.network.Ipv4Mask("255.255.255.0"))
interfaces = address.Assign(devices)

# Send secure message simulation
message = b"Hello VANET node"
msg, sig = secure_send(0, message)
is_valid = secure_receive(1, msg, sig)

print("Message Valid:", is_valid)

# Application simulation
echo_server = ns.applications.UdpEchoServerHelper(9)
server_apps = echo_server.Install(nodes.Get(1))
server_apps.Start(ns.core.Seconds(1.0))
server_apps.Stop(ns.core.Seconds(10.0))

echo_client = ns.applications.UdpEchoClientHelper(interfaces.GetAddress(1), 9)
echo_client.SetAttribute("MaxPackets", ns.core.UintegerValue(1))
echo_client.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds(1.0)))
echo_client.SetAttribute("PacketSize", ns.core.UintegerValue(1024))

client_apps = echo_client.Install(nodes.Get(0))
client_apps.Start(ns.core.Seconds(2.0))
client_apps.Stop(ns.core.Seconds(10.0))

# Run Simulation
ns.core.Simulator.Stop(ns.core.Seconds(11.0))
ns.core.Simulator.Run()
ns.core.Simulator.Destroy()
