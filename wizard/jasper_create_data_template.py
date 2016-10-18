from openerp import pooler
import base64
from openerp.osv import osv,fields
from openerp.tools.translate import _

class create_data_template(osv.osv_memory):
    _name = 'jasper.create.data.template'
    _description = 'Create data template'

    def action_create_xml(self, cr, uid, ids, context=None):
        for data in  self.read(cr, uid, ids, context=context):
            model = self.pool.get('ir.model').browse(cr, uid, data['model'][0], context=context)
            xml = self.pool.get('ir.actions.report.xml').create_xml(cr, uid, model.model, data['depth'], context)

        context['report_name'] = _('template.xml')
        context['report_data'] = base64.encodestring( xml )
        form_view = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'jasper_reports', 'view_pos_box_out1')

        return {
            'name': _('Jasper Reports'),
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'jasper.create.data.info',
            'target':'new',
            'view_id': False,
            'views': [(form_view and form_view[1] or False, 'form')],
            'type': 'ir.actions.act_window',
        }



    _columns = {
        'model': fields.many2one('ir.model', 'Model', required=True),
        'depth': fields.integer("Depth", required=True),
    }

    _defaults = {
        'depth': 1
    }
create_data_template()

class create_data_info(osv.osv_memory):
    _name = 'jasper.create.data.info'
    _columns = {
        'filename': fields.char('File Name', size=32),
        'data': fields.binary('XML')
    }

    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        res = super(create_data_info, self).default_get(cr, uid, fields, context=context)
        report_name = False
        report_data = False
        if context.get('report_name', False):
            report_name = context['report_name']
        if context.get('report_data', False):
            report_data = context['report_data']
        if 'data' in fields:
            res.update({'data': report_data})
        if 'filename' in fields:
            res.update({'filename': report_name})
        return res

create_data_info()