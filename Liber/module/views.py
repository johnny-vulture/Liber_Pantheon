from django.shortcuts import render
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Module, Page
from .serializers import ModuleSerializer
import PyPDF2


class ModuleCreateView(generics.CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        return render(request, 'module_form.html')

    def perform_create(self, serializer):
        pdf_file = self.request.data.get('pdf_file')
        code = self.request.data.get('code')

        # Create Module instance
        module = Module.objects.create(code=code)

        # Use PyPDF2 to extract data from PDF
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        total_pages = len(pdf_reader.pages)

        for page_num in range(total_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()

            # Create Page instances with extracted data
            Page.objects.create(
                page_number=page_num + 1,  # Page numbers are 1-based
                module=module,
                content=text)


class ModuleDetailView(generics.RetrieveAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    lookup_field = 'code'


class ModuleUpdateView(generics.UpdateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    lookup_field = 'code'


class ModuleDeleteView(generics.DestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    lookup_field = 'code'