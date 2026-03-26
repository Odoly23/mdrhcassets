import csv, io, datetime, json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.hashers import make_password
from config.decorators import allowed_users
from custom.models import Model, Brand, Category, SubCategory, BaseModel, Company, \
						  Ministerio, Year, Status, Location, Gabinete, DG, DN, \
						  Unidade, Entity, Departamento, StatusInv
from rir.models import RirItem
from staff.models import Employee
from django.contrib.auth.models import User
from assets.models import Asset
from django.utils import timezone
import hashlib
from config.utils import generate_barcode, getjustnewid, hash_md5
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from config.auth_utils import c_user_staff
from distribuition.models import Distribution

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from config.decorators import allowed_users
from rir.models import Rir

@login_required
@allowed_users(allowed_roles=['admin'])
def List_rir(request):
    group = request.user.groups.first().name if request.user.groups.exists() else None
    rirs = (Rir.active_objects.select_related("company", "created_by", "approved_by").prefetch_related(
            "items","items__category","items__sub_category","items__brand","items__model",).order_by("-id"))
    context = {
        'title': 'Lista Relatoriu Registo Inspeksaun',
        'legend': 'Lista Relatoriu Registo Inspeksaun',
        'group': group,
        'rirs': rirs,
        'menactive': "active",
        'link_antes': [{'link_name':"r-list",'link_text':"Rir"}],
    }
    return render(request, 'Rir/list_r.html', context)