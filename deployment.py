from modules.Path import Path


# Let's define how to deploy an application on the system.
def deployable_proc(proc, device):
    """
    Checks if a given process can be deployed onto a device.

    Args:
        proc : Processus
        device : Device

    Returns:
        Boolean, True if deployable, else False
    """
    if proc.cpu_request + device.cpu_usage < device.cpu_limit:
        if proc.gpu_request + device.gpu_usage < device.gpu_limit:
            if proc.mem_request + device.mem_usage < device.mem_limit:
                if proc.disk_request + device.disk_usage < device.disk_limit:
                    return True
    return False


def reservable_bandwidth(path, bandwidth_needed, physical_network_link_list):
    """
    Checks if a given bandwidth can be reserved along a given path.

    Args:
        path : Path
        bandwidth_needed : Bandwidth to allocate on the Path
        physical_network_link_list : List(PhysicalNetworkLink), List of physical links to evaluate the minimal bandwidth available on the Path 

    Returns:
        Boolean, True if bandwidth can be reserved, else False
    """
    return bandwidth_needed <= path.minBandwidthAvailableonPath(physical_network_link_list)


def linkability(deployed_app_list, proc_links, devices_list, physical_network_link_list):
    """
    Checks if a newly deployed processus can be linked to already deployed processus in a given app by checking the link quality on all Paths between the newly deployed processus and already deployed ones.

    Args:
        deployed_app_list : int, Device ID of the Device on which the last processus deployed
        proc_links : Application.proc_links, len(Application.num_procs)*len(Application.num_procs) matrix indicating necessary bandwidth on each virtual link between application processus members
        device_list : List of devices, used to get devices IDs and routing table, non modified (Global variable now, but globals are bad)
        physical_network_link_list : List(PhysicalNetworkLink), List of physical links to evaluate the minimal bandwidth available on the Path 

    Returns:
        Boolean, True if all the interconnexions are possible with given bandwidths, False if at least one is impossible.
    """
    new_device_id = deployed_app_list[-1]
    for i in range(len(deployed_app_list)):
        new_path = Path()
        new_path.path_generation(devices_list, new_device_id, deployed_app_list[i])
        if not reservable_bandwidth(new_path, proc_links[i][len(deployed_app_list)-1], physical_network_link_list):
            return False
    return True


def application_deploy(app, device, devices_list, physical_network_link_list):
    """
    Tries to deploy a multi-processus application from a given device

    Application will be deployed on device if possible, else the deployment will be tried on closest devices until all devices are explored

    Args:
        app : Application, application to deploy
        device : Device, first device to try deployment, \"Deployment Request Receptor\" device

    Returns:
        (deployment_success, latency, operational_latency, deployed_onto_devices)
            deployment_success : Bool, deployment success boolean
            latency : float, cumulative latency along deployment procedure
            operational_latency : float, cumulative latency between deployed processus based on links quality
            deployed_onto_devices : list, device ids for all devices onto application were deployed
    """

    deployment_success = True
    deployed = 0
    latency = 0
    operational_latency = 0
    # Get ordered device distance

    deployed_onto_devices = list()
    first_dev_exclusion_list = list()

    deployment_success = True

    tentatives = 0
    while len(deployed_onto_devices) < app.num_procs and tentatives < 2000:

        tentatives +=1

        if len(deployed_onto_devices) == 0 and len(first_dev_exclusion_list)==0:
            distance_from_device = {i: device.routing_table[i][1] for i in device.routing_table}
            sorted_distance_from_device = sorted(distance_from_device.items(), key=lambda x: x[1])
        else:
            if len(deployed_onto_devices)!= 0:
                new_source_device = devices_list[deployed_onto_devices[-1]]
            else:
                distance_from_device = {i: device.routing_table[i][1] for i in device.routing_table}
                if len(first_dev_exclusion_list) == len(distance_from_device):
                    deployment_success = False
                    break
                else:
                    for j in first_dev_exclusion_list:
                        if j in distance_from_device:
                            del distance_from_device[j]
                    sorted_distance_from_device = sorted(distance_from_device.items(), key=lambda x: x[1])
                    new_source_device = sorted_distance_from_device[0][0]

            distance_from_device = {i: new_source_device.routing_table[i][1] for i in new_source_device.routing_table}
            sorted_distance_from_device = sorted(distance_from_device.items(), key=lambda x: x[1])


        for device_id, deployment_latency in sorted_distance_from_device:
            if deployable_proc(app.processus_list[len(deployed_onto_devices)], devices_list[device_id]):
                deployed_onto_devices.append(device_id)

                if linkability(deployed_onto_devices, app.proc_links, devices_list, physical_network_link_list):

                    # deploy on device
                    device_deployed_onto = devices_list[device_id]

                    device_deployed_onto.setDeviceCPUUsage(device_deployed_onto.cpu_usage + app.processus_list[len(deployed_onto_devices)-1].cpu_request)
                    device_deployed_onto.setDeviceGPUUsage(device_deployed_onto.gpu_usage + app.processus_list[len(deployed_onto_devices)-1].gpu_request)
                    device_deployed_onto.setDeviceDiskUsage(device_deployed_onto.disk_usage + app.processus_list[len(deployed_onto_devices)-1].disk_request)
                    device_deployed_onto.setDeviceMemUsage(device_deployed_onto.mem_usage + app.processus_list[len(deployed_onto_devices)-1].mem_request)

                    devices_list[device_id] = device_deployed_onto

                    # deploy links
                    for i in range(len(deployed_onto_devices)):
                        new_path = Path()
                        new_path.path_generation(devices_list, device_id, deployed_onto_devices[i])
                        for path_id in new_path.physical_links_path:
                            if physical_network_link_list[path_id] is not None:
                                physical_network_link_list[path_id].useBandwidth(app.proc_links[len(deployed_onto_devices)-1][i])
                                operational_latency += physical_network_link_list[path_id].getPhysicalNetworkLinkLatency()
                            else:
                                print("Error here, proper error to add, should be unreachable for now")


                    # get values

                    latency = deployment_latency
                    deployed +=1

                    break
                else:
                    deployed_onto_devices.pop()

    if (not deployment_success) or (tentatives == 2000):
        for i in range(len(deployed_onto_devices)):
            device_id = deployed_onto_devices[i]

            device_deployed_onto = devices_list[device_id]

            device_deployed_onto.setDeviceCPUUsage(device_deployed_onto.cpu_usage - app.processus_list[i].cpu_request)
            device_deployed_onto.setDeviceGPUUsage(device_deployed_onto.gpu_usage - app.processus_list[i].gpu_request)
            device_deployed_onto.setDeviceDiskUsage(device_deployed_onto.disk_usage - app.processus_list[i].disk_request)
            device_deployed_onto.setDeviceMemUsage(device_deployed_onto.mem_usage - app.processus_list[i].mem_request)

            devices_list[device_id] = device_deployed_onto

        deployment_success = False
        latency = 0
        operational_latency = 0
        deployed_onto_devices = list()

    if len(deployed_onto_devices) !=0:
        print(f"application id : {app.id} , {app.num_procs} processus deployed on {deployed_onto_devices}")
    else:
        print(f"application id : {app.id} , {app.num_procs} processus not deployed")

    return deployment_success, latency, operational_latency, deployed_onto_devices
