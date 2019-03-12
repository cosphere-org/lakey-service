
# from django.views.generic import View
# from lily import (
#     command,
#     Input,
#     Meta,
#     name,
#     Output,
# )

# from .domains import DOWNLOAD_PROCESSES
# from .models import DownloadProcess
# from .serializers import DownloadProcessSerializer
# from .parsers import DownloadProcessParser


# class DownloadProcessElementView(View):

#     @command(
#         name=name.Read(DownloadProcess),

#         meta=Meta(
#             title='...',
#             domain=DOWNLOAD_PROCESSES),

#         output=Output(serializer=DownloadProcessSerializer),
#     )
#     def get(self, request, process_id):

#         return self.event.Read(DownloadProcess.objects.get(process_id))


# class DownloadProcessCollectionView(View):

#     @command(
#         name=name.Create(DownloadProcess),

#         meta=Meta(
#             title='...',
#             domain=DOWNLOAD_PROCESSES),

#         input=Input(body=DownloadProcessParser),

#         output=Output(serializer=DownloadProcessSerializer),
#     )
#     def post(self, request):

#         process, _ = DownloadProcess.objects.get_or_create(
#             download_spec=request.body['download_spec'])

#         return self.event.Created(process)


# class DownloadProcessEstimateView(View):

#     @command(
#         name=name.Execute('ESTIMATE', 'SIZE_OF_DOWNLOAD_PROCESS'),

#         meta=Meta(
#             title='...',
#             domain=DOWNLOAD_PROCESSES),

#         input=Input(body=DownloadProcessParser),

#         output=Output(serializer=DownloadProcessSerializer),
#     )
#     def post(self, request):

#         download_spec = request.body['download_spec']

#         estimated_size = DownloadProcess.objects.estimate_size(
#             download_spec=download_spec)

#         return self.event.Executed({'estimated_size': estimated_size})
