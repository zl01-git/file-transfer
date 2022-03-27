import logging
import sys
import os
import seqlog
import grpc
import file_transfer_pb2 as ft_pb2
import file_transfer_pb2_grpc as ft_pb2_grpc


PATH_DOWNLOAD = os.path.abspath('client_file/')

def file_download(stub):
    responce_stream = stub.FileDownload(ft_pb2.FileDownloadReq(name='first_server_file.bin'))
    for responce in responce_stream:
        file_name = responce.name
        size = responce.size
    with open(PATH_DOWNLOAD + file_name, 'wb') as wf:
        for responce in responce_stream:
            wf.write(responce.data)
    logger.info(f'{file_name} {size}B saved to {PATH_DOWNLOAD}')
    
def get_file_list(stub):
    logger.debug('Getting a list of files from server')
    file_list, count = [], 1
    responce_stream = stub.GetFileList(ft_pb2.GetListReq())
    for responce in responce_stream:
        file_list.append((count, responce.name))
        count += 1
    logger.debug('The list of files was successfully recived')
    logger.debug(file_list)

def run():
    with grpc.insecure_channel('localhost:2352') as channel:
        stub = ft_pb2_grpc.FileServerStub(channel)
        
        get_file_list(stub)
        # file_download(stub)



    pass

if __name__ == '__main__':
    logger = logging.getLogger('log.client')
    fh = logging.StreamHandler(sys.stdout)
    format = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s() %(message)s')
    fh.setFormatter(format)
    logger.addHandler(fh)
    logger.setLevel(10)
    logger.debug('run() was running')
    run()