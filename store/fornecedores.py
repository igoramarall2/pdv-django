from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Vendas, VendaProduto, Produto
from django.db import transaction
import json
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings
import os

