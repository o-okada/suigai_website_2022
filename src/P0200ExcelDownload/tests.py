from django.test import TestCase
from django.urls import reverse

from P0000Common.models import KEN
from P0000Common.common import print_log

class IndexViewTests(TestCase):
    def test_index_view(self):
        url = reverse('P0200ExcelDownload:index_view', )
        response = self.client.get(url)
        print_log('[INFO] P0200ExcelDownload.IndexViewTests response.context[ken_list] = {}'.format(response.context['ken_list']), 'INFO')
        print_log('[INFO] P0200ExcelDownload.IndexViewTests response.context[city_list01] = {}'.format(response.context['city_list01']), 'INFO')
        ### ken = KEN.objects.create()
        self.assertEqual(response.status_code, 200)
        ### self.assertQuerysetEqual(response.context['ken_list'], [ken],)
        
    def test_building_view(self):
        url = reverse('P0200ExcelDownload:building_view', )
        response = self.client.get(url)
        ### print_log('[INFO] P0200ExcelDownload.IndexViewTests.test_building_view response = {}'.format(response), 'INFO')
        self.assertEqual(response.status_code, 200)