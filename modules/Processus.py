import random

class Processus:
    # A processus is a sub-part of an application
    def __init__(self) -> None:
        # Initializes the processus with basic value

        # ID set to -1
        self.id = -1

        # A process requests ressources among the 4 resources defined : CPU, GPU, Memory and Disk
        self.cpu_request = 0
        self.gpu_request = 0
        self.mem_request = 0 * 1024
        self.disk_request = 0 * 1024

    def setProcessusID(self, id):
        # Set processus ID
        self.id = id

    def getProcessusID(self):
        # Returns processus ID
        return self.id

    def setProcessusCPURequest(self, cpu):
        # Sets CPU Request
        self.cpu_request = cpu

    def setProcessusGPURequest(self, gpu):
        # Sets GPU Request
        self.gpu_request = gpu

    def setProcessusMemRequest(self, mem):
        # Sets Memory Request
        self.mem_request = mem

    def setProcessusDiskRequest(self, disk):
        # Sets Disk Space Request
        self.disk_request = disk

    # Random processus initialization
    def randomProcInit(self):
        # Random number of CPU between 0.5 and 4
        self.setProcessusCPURequest(random.choice([0.5,1,2,3,4]))
        # Random number of GPU between 0 and 8
        self.setProcessusGPURequest(random.choice([0,0.5,1,4,6,8]))
        # Random Memory between 0.1 and 4 GigaBytes
        self.setProcessusMemRequest((random.random() * 0.975 + 0.025) * 4 * 1024)
        # Random Disk space between 10 and 100 GigaBytes
        self.setProcessusDiskRequest((random.random() * 9 + 1) * 10 * 1024)

    def processus_yaml_parser(self, processus_yaml):

        processus_content = processus_yaml['Processus']

        self.setProcessusCPURequest(processus_content['cpu'])
        self.setProcessusGPURequest(processus_content['gpu'])
        self.setProcessusMemRequest(processus_content['memory'])
        self.setProcessusDiskRequest(processus_content['disk'])