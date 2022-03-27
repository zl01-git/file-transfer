from concurrent import futures
import logging
import seqlog
import sys
import os
import grpc

import file_transfer_pb2 as ft_pb2
import file_transfer_pb2_grpc as ft_pb2_grpc


class FileServ(ft_pb2_grpc.FileServerServicer):
    PIECE_OF_FILE = 1024 * 1024
    PATH = '/home/zl01/file_transfer/server_file/'

    def FileDownload(self, request, context):
        logger.debug(f'preparing to send the file {request.name} to the client')        
        absolute_name = FileServ.PATH + request.name
        file_name = request.name
        size = os.path.getsize(absolute_name)

        with open (absolute_name, 'rb') as fl:
            while True:
                piece = fl.read(FileServ.PIECE_OF_FILE)
                if len(piece) == 0:
                    break
                yield ft_pb2.FileDownloadRsp(data=piece, name=file_name, size=size)
        logger.info(f'{request.name} successfully sending')

    def GetFileList(self, request, context):
        logger.debug('preparing to send the list files to the client')
        for item in os.listdir(FileServ.PATH):
            name = item
            size = os.path.getsize(FileServ.PATH + item)
            yield ft_pb2.GetListRsp(name=name, size=size)
        logger.info('list files was sending')
        pass

    def FileUpload(self, request_iterator, context):
        
        pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ft_pb2_grpc.add_FileServerServicer_to_server(FileServ(), server)
    server.add_insecure_port('[::]:2352')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logger = logging.getLogger('log.server')
    fh = logging.StreamHandler(sys.stdout)
    format = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s() %(message)s')
    fh.setFormatter(format)
    logger.addHandler(fh)
    logger.setLevel(10)
    logger.debug('serve() was running')
    serve()