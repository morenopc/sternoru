#!/usr/bin/python
# -*- coding: UTF8 -*-

from django.contrib import admin
from api.models import Profile, Place, Checkin

#class ProfileAdmin(admin.ModelAdmin):
#    list_display=['data','CI','nome','munic','bairro','logradTipo','lograd','num','ponto_ref','tel','cel','CPF','nis','medidor','criado_em','nome_pesq','n_pessoas','renda_familiar','renda_per_capita','imovel_uso','imovel_ocupacao','imovel_danos','ar_cond','chuv','ferro','freez','gela','liqui','maq_lavar','micro','som','tanq','tv','vent','lamps','chuv_potencia','chuv_banho','chuv_banho_p_dia','chuv_banho_duracao','chuv_banho_freq_noite','gela_tam','gela_idade','gela_termostato','gela_tampa_congelador','gela_porta_fecha','gela_veda_porta','pontuacao','lamp_incan_25','lamp_incan_40','lamp_incan_60','lamp_incan_100','lamp_incan_150','lamp_incan_200','lamp_fluor_c_9','lamp_fluor_c_15','lamp_fluor_c_20','lamp_fluor_c_40','lamp_fluor_t_20','lamp_fluor_t_40','concorda','instal_eq','outro_resp','resp_nome','resp_tel']
#    list_display_links = ('nome',)
#    search_fields = ['id','nome']
#    list_filter = ('criado_em',)
    #date_hierarchy = 'criado_em'
    #ordering = ['-cad_bl1Data']

admin.site.register(Profile)
admin.site.register(Place)
admin.site.register(Checkin)
