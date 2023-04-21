"""
Device module, defines the Device Class

Usage:

"""
class Device:
    # An Device is defined as a group of values : CPU, GPU, Memory, Disk space
    # Each value is set twice, the maximal value as #_limit and current_use as #_usage
    # Additionally, each device has a form of routing table, the routing table stores the next_hop value and distance from the device to each other device in the network

    # Devices have a given id

    id = 0


    @classmethod
    def _generate_id(cls):
        """
        Class method for id generation
        Assigns id then increment for next generation

        Args:
            None

        Returns:
            result : int, Device ID
        """
        result = cls.id
        cls.id +=1
        return result


    def __init__(self) -> None:
        """
        Initializes the device with basic values
        Assigns ID, initial position, resource values, routing table and resource limits

        Args:
            None

        Returns:
            None
        """
        # ID setting
        self.id = Device._generate_id()

        # Device Position in the area considered
        self.x = 0
        self.y = 0
        self.z = 0

        # Maximal limit for each device feature
        ## CPU Limit (int) in number of CPUs, initialized to 2
        self.cpu_limit = 2
        ## GPU Limit (int) in number of GPUs, initialized to 2
        self.gpu_limit = 2
        ## RAM (int) in MegaBytes, initialized to 4 GigaBytes
        self.mem_limit = 4 * 1024
        ## Disk size (int) in MegaBytes, initialized to 250 GigaBytes
        self.disk_limit = 250 * 1024

        # Current usage for each device feature
        ## CPU Usage (float) in number of CPUs, initialized to 0
        self.cpu_usage = 0
        ## GPU Usage (float) in number of GPUs, initialized to 0
        self.gpu_usage = 0
        ## RAM Usage (float) in MegaBytes, initialized to 0
        self.mem_usage = 0
        ## Disk Usage (float) in MegaBytes, initialized to 0
        self.disk_usage = 0

        # Routing table, dict {destination:(next_hop, distance)}
        ## Initialized to {self.id:(self.id,0)} as route to self is considered as distance 0
        self.routing_table = {self.id:(self.id,0)}

    def setDeviceID(self, id):
        """
        Used to set a device's ID by hand if necessary
        This will reinitialize the device's routing table to {self.id:(self.id,0)}

        Args:
            id : int, new device ID

        Returns:
            None
        """
        self.id = id
        self.routing_table = {self.id:(self.id,0)}

    def getDeviceID(self):
        """
        Returns device ID

        Args:
            None

        Returns:
            id : int, device ID
        """
        return self.id

    def setDevicePosition(self, x, y, z):
        """
        Sets device position in a 3D space

        Args:
            x : float, position along x axis
            y : float, position along y axis
            z : float, position along z axis

        Returns:
            None
        """
        self.x = x
        self.y = y
        self.z = z


    def setDeviceCPULimit(self, cpu):
        """
        Sets Device CPU Limit

        Args:
            cpu : int, number of CPUs to set as device maximal limit

        Returns:
            None
        """
        self.cpu_limit = cpu

    def setDeviceGPULimit(self, gpu):
        """
        Sets Device GPU Limit

        Args:
            gpu : int, number of GPUs to set as device maximal limit

        Returns:
            None
        """
        self.gpu_limit = gpu

    def setDeviceMemLimit(self, mem):
        """
        Sets Device Memory Limit

        Args:
            mem : int, quantity of memory to set as device maximal limit, in MBytes

        Returns:
            None
        """
        self.mem_limit = mem

    def setDeviceDiskLimit(self, disk):
        """
        Sets Device Disk Space Limit

        Args:
            mem : int, quantity of disk space to set as device maximal limit, in GBytes

        Returns:
            None
        """
        self.disk_limit = disk


    def setDeviceCPUUsage(self, cpu):
        """
        Sets Device CPU Usage

        Args:
            cpu : float, value for the quantity of CPU used by device

        Returns:
            None
        """
        self.cpu_usage = cpu

    def setDeviceGPUUsage(self, gpu):
        """
        Sets Device GPU Usage

        Args:
            gpu : float, value for the quantity of GPU used by device

        Returns:
            None
        """
        self.gpu_usage = gpu

    def setDeviceMemUsage(self, mem):
        """
        Sets Device Memory Usage

        Args:
            mem : float, value for the quantity of memory used by device, in MBytes

        Returns:
            None
        """
        self.mem_usage = mem

    def setDeviceDiskUsage(self, disk):
        """
        Sets Device Disk Space Usage at time t

        Args:
            disk : float, value for the quantity of disk space used by device, in GBytes

        Returns:
            None
        """
        self.disk_usage = disk

    # Generates a rounting table progressively by adding devices
    # Path are not considered, only next hop and distance
    # Single path for now
    def addToRoutingTable(self, destination_id, next_hop_id, distance_destination):#, distance_next_hop):
        """
        Adds a new destination or update an existing one in the routing table
        Reminder - routing table element are : {destination:(next_hop, distance)}

        Args:
            destination_id : int, Device ID of the destination point
            next_hop_id : int, Device ID of the next hop in the path to destination
            distance_destination : int, distance from device (self) to destination (destination_id), when passing through device (next_hop_id), distance is arbitrary, can be actual distance, number of hops, ...

        Returns:
            None
        """
        # First we check if the destination is already in the table
        if destination_id in self.routing_table:
            # We check if we need to change the existing value
            if distance_destination < self.routing_table[destination_id][1]:
                # Update the existing value if the new one is lower (the lower the better)
                self.routing_table[destination_id] = (next_hop_id,distance_destination)
        else:
            # Add the new value if no previous value
            self.routing_table[destination_id] = (next_hop_id,distance_destination)

    # Returns the values associated to the route from the device to the destination
    def getRouteInfo(self, destination_id):
        """
        Returns the values associated to the route from the device to the destination

        Args:
            destination_id : int, Device ID of the destination point

        Returns:
            (next_hop, distance) : (int, float), next hop in the routing table to reach destination, distance from host to destination

        Raises:
            DestinationUnknown: If destination is not in routing table -- To Be Implemented
        """
        # We check if the destination is known
        if destination_id in self.routing_table:
            # If it is known, we return the associated values
            return self.routing_table[destination_id]
        else:
            """
            raise DestinationUnknownError(
                f'No route to host {destination_id}'
            )
            """
            # If not, we return placeholder values (device_id = -1 and distance = 1000)
            # We might change this to raise and error such as "no route to host"
            return (-1, 1000)

