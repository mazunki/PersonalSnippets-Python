def get_default_network():
    available_network = input("Name the network you have available:\nA for 10.0.0.0/8 \nB for 172.16.0.0/16\nC for 192.168.1.0/24 [default]\nCustom network IP supported. Dot-decimal netmask can be used if CIDR not included. \n> ")
    if available_network.lower() == "a":
        network_ip = "10.0.0.0"
        default_mask = "8"
    elif available_network.lower() == "b":
        network_ip = "172.16.0.0"
        default_mask = "16"
    elif available_network.lower() in ["c", ""]:
        network_ip = "192.168.1.0"
        default_mask = "24"
    elif "/" not in available_network:
        default_mask = input("What's the given network mask?")
        if "/" not in default_mask and default_mask.count(".")==3:
            default_mask = default_mask.strip()
            octets = [int(val) for val in default_mask.split(".")]
            bin_octets = list()
            for octet in octets:
                if octet<256 and octet>=0:
                    binarial_form = "{0:08b}".format(octet)
                    bin_octets.append(binarial_form)
                else:
                    print("Invalid subnet mask. Range must be 0-255 for all octets.")

            for octet in bin_octets:
                if octet == "".join(sorted(octet,reverse=True)):  # 1s must be at the start of all octets
                    pass
                else:
                    print("Invalid subnet mask. Possible values are 0, 128, 192, 224, 240, 248, 252, 254, 255.")

            found_first_zero = False
            default_mask = 0
            for octet in bin_octets:
                if "0" in octet:
                    found_first_zero = True
                elif found_first_zero and octet is not "00000000":
                    print("Invalid subnet mask. Network masks must be left-trailed.")
                default_mask += octet.count("1")

            if found_first_zero == False:
                print("This is a broadcast address.")


            #print("Binarial form of network mask: ",end="")
            #print(*bin_octets,sep=".")
        elif default_mask.count(".")!=3 and "/" not in default_mask:
            print("Invalid mask. Only 4 octets are allowed.")
        else:
            if available_network.count("/") == 1:
                network_ip, default_mask = available_network.split("/")
                default_mask = int(default_mask)
                if default_mask>0 and default_mask<32:
                    binary_mask = "{:<032d}".format(int("1"*default_mask))
                    bin_octets = [binary_mask[start:start+8] for start in range(0, 32, 8)]
                    #print(bin_octets)
                elif default_mask==32:
                    print("This is a broadcast address.")
            else:
                print("Invalid address. Only one / allowed.")
    else:
        if available_network.count("/") == 1:
            network_ip, default_mask = available_network.split("/")
            default_mask = int(default_mask)
            if default_mask>0 and default_mask<32:
                binary_mask = "{:<032d}".format(int("1"*default_mask))
                bin_octets = [binary_mask[start:start+8] for start in range(0, 32, 8)]
                #print(bin_octets)
            elif default_mask==32:
                print("This is a broadcast address.")
            else:
                print("/0 is not allowed.")
        else:
            print("Invalid address. Only one / allowed.")

    return network_ip, int(default_mask)

def flsm():
    network_ip, default_mask = get_default_network()
    print("Let's configure your network: ", network_ip, "/", default_mask, sep="")

    print("What do you want to define? ")
    selection = input("1. Number of subnets\n2. Number of hosts\n")
    if selection.lower() in ["1", "networks", "n", "netw", "subnets", "subnetworks"]:
        number_of_networks = int(input("How many networks do you need? "))

        minimum_size = 1
        bits_needed = 0
        while minimum_size < number_of_networks:
            minimum_size *= 2
            bits_needed += 1
        print(minimum_size, bits_needed)
        total_bits = default_mask + bits_needed
        binary_subnet_mask = "{:<032d}".format(int("1"*total_bits))
        binary_subnet_mask_formatted = " ".join([binary_subnet_mask[start:start+8] for start in range(0, 32, 8)])
    elif selection.lower() in ["2", "hosts", "h", "host"]:
        number_of_hosts = int(input("How many hosts do you need per network? "))+2  # + Broadcast + Network name

        minimum_hosts = 1
        bits_needed = 0
        while minimum_hosts < number_of_hosts:
            minimum_hosts *= 2
            bits_needed += 1
        print(minimum_hosts, bits_needed)
        total_bits = 32 - bits_needed
        binary_subnet_mask = "{:<032d}".format(int("1"*total_bits))
        binary_subnet_mask_formatted = " ".join([binary_subnet_mask[start:start+8] for start in range(0, 32, 8)])

    print("Your subnet mask should be:", binary_subnet_mask_formatted, "==", ".".join([str(int(binary_subnet_mask[start:start+8], 2)) for start in range(0, 32, 8)]))
    print("Your network will be defined as: ", network_ip, "/", total_bits, sep="")
    n_subnets = 2**(total_bits-default_mask)
    n_hosts = 2**(32-total_bits)

    print("You will have {} subnets available in {}/{}, \nwith{: } hosts in each.".format(n_subnets, network_ip, default_mask, n_hosts))



def vlsm():
    network_ip, default_mask = get_default_network()
    size_network = 2**(32-default_mask)

    def ip_to_binary(ipv4):
        ipv4_octets = ipv4.split(".")
        binary_stuff = ""
        for octet in ipv4_octets:
            binary_stuff += "{0:08b}".format(int(octet))

        return int(binary_stuff, 2)

    def binary_to_ip(binip):
        rawbinary = "{0:032b}".format(binip)
        octets = ".".join([str(int(rawbinary[start:start+8],2)) for start in range(0,32,8)])
        return octets


    print("Input the number of hosts of each network on a new line, finish with 0.\n")

    subnets = list()
    while (subnets or [None])[-1] != 0:
        subnets.append(int(input("> ")))

        if subnets[-1] > 2**(32-default_mask):
            print("Too big for this network.")

    subnets.pop(-1)  # Remove 0 sized network
    subnets = sorted(subnets, reverse=True)

    index = 0
    subnets_dict = dict()
    first_available_ip = network_ip
    for subnet in subnets:
        minimum_hosts = 1
        bits_needed = 0
        while minimum_hosts < subnet:
            minimum_hosts *= 2
            bits_needed += 1
        total_bits = 32 - bits_needed

        last_ip_of_range = binary_to_ip(ip_to_binary(first_available_ip)+minimum_hosts-1)

        subnets_dict[index] = { "Size: ": minimum_hosts, 
                                "Bits: ": bits_needed, 
                                "First ip in range: ": first_available_ip, 
                                "Last ip in range: ": last_ip_of_range}
        index += 1
        first_available_ip = binary_to_ip(ip_to_binary(last_ip_of_range)+1)

    for subnet, details in subnets_dict.items():
        print(subnet, ":", sep="")
        for item, info in details.items():
            print(" "*4, item, ": ", info, sep="")

    first_unused = binary_to_ip(ip_to_binary(subnets_dict[index-1]["Last ip in range: "])+1)
    last_of_network = binary_to_ip(ip_to_binary(network_ip) + size_network -1)
    print("\nRange", first_unused, "to", last_of_network, "are unused.")


if __name__ == '__main__':
    print("""Welcome to the subnet mask creator. \nDo you want a FLSM setup, or a VLSM setup?\n""")
    type_scheme = input("1. FLSM [default]\n2. VLSM\n")

    while True:
        if type_scheme.lower() in ["1", "flsm", ""]:
            print("You selected a FLSM scheme.")
            flsm()
            break
        elif type_scheme.lower() in ["2", "vlsm"]:
            print("You selected a FLSM scheme.")
            vlsm()
            break
        else:
            print("Invalid option.")