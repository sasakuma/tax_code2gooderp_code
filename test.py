# -*- coding: utf-8 -*-
from lxml import etree


def changexml():
    tree = etree.parse('spfwssflbm.xml')
    openerp = etree.Element('openerp')
    data = etree.SubElement(openerp, 'data')
    list = []
    ncols = 0
    for bbox in tree.xpath('//BMXX'):  # 获取BMXX元素的内容
        app = {}
        ncols += 1
        for corner in bbox.getchildren():  # 便利BMXX元素下的子元素
            try:
                app[corner.tag] = corner.text
            except:
                continue
        if app.get('KYZT'):
            list.append(app)

    in_xml_data = {}
    m = 0
    i = {}
    n = []
    for m in range(0, ncols):
        in_xml_data = list[m]
        if in_xml_data.get('ZZSTSGL'):
            base_category = in_xml_data.get('ZZSTSGL')
            if base_category in n:
                continue
            else:
                m += 1
                category = 'tax_base_category%s' % m
                record2 = etree.SubElement(data, 'record',
                                           attrib={'id': category, 'model': "tax.base.category"})
                field2 = etree.SubElement(record2, 'field', attrib={'name': 'name'})
                field2.text = in_xml_data.get('ZZSTSGL')
                i[base_category] = category
                n.append(base_category)

    in_xml_data = {}
    for d in range(0, ncols):
        in_xml_data = list[d]
        if in_xml_data.get('SPBM'):
            record = etree.SubElement(data, 'record', attrib={'id': 'nsbm%s' %in_xml_data.get('SPBM'), 'model': "tax.category"})
        if in_xml_data.get('HZX'):
            field = etree.SubElement(record, 'field', attrib={'name': 'can_use'})
            if in_xml_data.get('HZX') == 'Y':
                field.text = 'False'
            else:
                field.text = 'True'
        if in_xml_data.get('SPMC'):
            field = etree.SubElement(record, 'field',attrib={'name': 'name'})
            field.text = in_xml_data.get('SPMC')
        if in_xml_data.get('SPBMJC'):
            field = etree.SubElement(record, 'field', attrib={'name': 'print_name'})
            field.text = in_xml_data.get('SPBMJC')
        if in_xml_data.get('SPBM'):
            field = etree.SubElement(record, 'field', attrib={'name': 'code'})
            field.text = in_xml_data.get('SPBM')
        if in_xml_data.get('SM'):
            field = etree.SubElement(record, 'field', attrib={'name': 'note'})
            field.text = in_xml_data.get('SM')
        if in_xml_data.get('GJZ'):
            field = etree.SubElement(record, 'field', attrib={'name': 'help'})
            field.text = in_xml_data.get('GJZ')
        if in_xml_data.get('ZZSSL'):
            field = etree.SubElement(record, 'field', attrib={'name': 'tax_rate'})
            field.text = in_xml_data.get('ZZSSL')
        if in_xml_data.get('PID') == '0':
            pass
        else:
            field = etree.SubElement(record, 'field', attrib={'name': 'superior', 'ref':'nsbm%s' %in_xml_data.get('PID')})
        if in_xml_data.get('ZZSTSGL'):
            base_category = in_xml_data.get('ZZSTSGL')
            if i.get(base_category):
                field = etree.SubElement(record, 'field',attrib={'name': 'base_category', 'ref': i.get(base_category)})

    tree = etree.ElementTree(openerp)
    tree.write('tax_code.xml', pretty_print=True, xml_declaration=True, encoding='UTF-8')

if __name__ == "__main__":
    changexml()