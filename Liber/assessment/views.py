import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.shortcuts import redirect
from django.urls import reverse
from .models import Assessment, Question, Section
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


class UploadView(View): 
    template_name = 'upload_json.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        json_file = request.FILES.get('json_file')
        if json_file:
            json_data = json_file.read().decode('utf-8')
            display_url = reverse('display') + f'?data={json_data}'
            return redirect(display_url)
        return JsonResponse(data={'error': 'No JSON file provided.'},
                            status=400)


class UploadJSONView(View):
    template_name = 'upload_json.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        try:
            uploaded_json = json.loads(
                request.FILES.get('json_file').read().decode('utf-8'))

            assessment_name = uploaded_json.get('assessment')
            unique_code = uploaded_json.get('unique_code')

            if assessment_name and unique_code:
                assessment = Assessment.objects.create(name=assessment_name,
                                                       unique_code=unique_code)

                questions = uploaded_json.get('questions', [])

                for question_data in questions:
                    question_text = question_data.get('question')
                    module_code = question_data.get('module_code')
                    sub_questions = question_data.get('sub_questions', [])

                    if question_text:
                        question = Question.objects.create(
                            assessment=assessment,
                            header=question_text,
                            module_code=module_code)

                        for sub_question_text in sub_questions:
                            # Create Section and set reference using get_answer_from_reference
                            section = Section.objects.create(question=question,
                                                             sub_q=sub_question_text)
                            section.get_answer_from_reference()
                            section.save()  # Save the section to update the reference

                return redirect(reverse('assessment_list'))
            else:
                return JsonResponse(
                    {'error': 'Assessment name and unique code are required.'},
                    status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class AssessmentListView(View):
    template_name = 'assessment_list.html'

    def get(self, request, *args, **kwargs):
        assessments = Assessment.objects.all()
        return render(request, self.template_name,
                      {'assessments': assessments})


class CreateAssessmentView(View):
    template_name = 'upload_form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        try:
            assessment_name = request.POST.get('assessment')
            unique_code = request.POST.get('uniqueCode')
            questions = request.POST.getlist('questions[]')

            assessment_data = {
                "assessment": assessment_name,
                "unique_code": unique_code,
                "questions": []
            }

            for question in questions:
                question_data = {
                    "question":
                    question,
                    "module_code":
                    request.POST.get(f"{question}-module_code"),
                    "sub_questions":
                    request.POST.getlist(f"{question}-sub_questions[]")
                }
                assessment_data["questions"].append(question_data)

            json_data = json.dumps(assessment_data, indent=4)

            return JsonResponse({'success': 'JSON file created successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class GeneratePDFTemplateView(View):
    template_name = 'generate_pdf.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class GeneratePDFView(View):
    def get(self, request, *args, **kwargs):
        assessment_name = request.GET.get('assessment_name')
        unique_code = request.GET.get('unique_code')

        assessment = get_object_or_404(
            Assessment, name=assessment_name, unique_code=unique_code)
        questions = Question.objects.filter(assessment=assessment)

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)

        # Write assessment and unique_code
        pdf.drawString(100, 750, f"Assessment: {assessment_name}")
        pdf.drawString(100, 730, f"Unique Code: {unique_code}")

        # Write questions and sections
        y_position = 700
        max_line_width = 400  # Adjust this value based on your layout
        line_height = 15  # Adjust this value based on your layout

        for question in questions:
            y_position -= line_height
            pdf.setFont("Helvetica", 12)  # Set font and size for wrapping text
            pdf.drawString(15, y_position, f"Question: {question.header}")
            y_position -= line_height
            sections = Section.objects.filter(question=question)
            for section in sections:
                y_position -= line_height
                pdf.drawString(20, y_position, f"sub_q:")
                y_position -= line_height
                sub_q_lines = self.wrap_text(section.sub_q, max_line_width)
                for sub_q_line in sub_q_lines:
                    pdf.drawString(20, y_position, sub_q_line)
                    y_position -= line_height
                pdf.drawString(20, y_position, f"reference:")
                y_position -= line_height
                reference_lines = self.wrap_text(
                    section.reference, max_line_width)
                for reference_line in reference_lines:
                    pdf.drawString(20, y_position, reference_line)
                    y_position -= line_height
            y_position -= line_height

        pdf.save()
        buffer.seek(0)

        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{assessment_name}_report.pdf"'
        return response

    def wrap_text(self, text, max_width):
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            if sum(len(w) for w in current_line) + len(current_line) + len(word) <= max_width:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))

        return lines
