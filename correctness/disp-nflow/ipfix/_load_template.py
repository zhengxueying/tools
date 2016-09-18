# encoding: utf-8

from ipfix._obj import LogObj
from ipfix import KEY_FIELDS_DEF, KEY_FIELDS_LEN, FLD_NAME, FLD_ID, FLD_ENT_NUM, FLD_LEN, FLD_END_E_MASK, SOURCE_ID, \
    TEMP_ID, FLD_CNT, REC_SIZE
from ipfix._fielddef import IpfixFieldDef


def load_template(fp, **kwargs):
    # init template
    temp = {SOURCE_ID: 0, TEMP_ID: 0, REC_SIZE: 0, FLD_CNT: 0}
    fields_size = 0
    fields = []

    # iterate template file
    for l in fp.readlines():
        l = l.strip()
        if ':' in l:
            if len(fields) > 0:
                if fields_size == temp[REC_SIZE]:
                    # current template is completed
                    temp[FLD_CNT] = len(fields)
                    yield temp, fields
                # init again
                temp = {SOURCE_ID: 0, TEMP_ID: 0, REC_SIZE: 0, FLD_CNT: 0}
                fields_size = 0
                fields = []

            key_value = l.split(":")
            if len(key_value) != 2:
                continue
            key = key_value[0].strip()
            value = key_value[1].strip()
            if key == 'Template ID':
                temp[TEMP_ID] = int(value)
            elif key == 'Source ID':
                temp[SOURCE_ID] = int(value)
            elif key == 'Record Size':
                temp[REC_SIZE] = int(value)

        elif l.startswith('|'):
            obj = _parse_temp_field(len(fields), l)
            if obj:
                fields.append(obj)
                fields_size += obj[FLD_LEN]

    if fields_size == temp[REC_SIZE]:
        # current template is completed
        temp[FLD_CNT] = len(fields)
        yield temp, fields


def _parse_temp_field(index, line):
    segs = [s.strip() for s in line.split("|")[1:6]]
    obj = IpfixFieldDef(0)
    if obj.load_from_template(index, segs):
        return obj
    return None


def dump_template(fp, global_template, **kwargs):
    dumper = IpfixTemplateDumper(fp)
    dumper.execute(fp, global_template, **kwargs)

INDENT = "  "


class IpfixTemplateDumper(LogObj):

    def __init__(self, fp):
        super(IpfixTemplateDumper, self).__init__()
        self.fp = fp

    def execute(self, fp, global_template, **kwargs):
        self.write_line("Dump templates by disp-nflow")
        for key, temp_obj in global_template.iteritems():
            source_id, temp_id = key
            self._dump_template(source_id, temp_id, temp_obj, **kwargs)

    def write_line(self, *msg):
        if isinstance(msg, str):
            self.fp.write(str(msg) + "\n")
        else:
            self.fp.write("".join([str(m) for m in msg]) + "\n")

    def _dump_template(self, source_id, temp_id, temp_obj, **kwargs):
        self.write_line("Dump template %d:" % temp_id)
        self.write_line("  Template ID    : ", temp_id)
        self.write_line("  Source ID      : ", source_id)
        self.write_line("  Record Size    : ", temp_obj.get(KEY_FIELDS_LEN))
        self.write_line("  Template layout")
        self.write_line("  _____________________________________________________________________________")
        self.write_line("  |                 Field                   |    ID | Ent.ID | Offset |  Size |")
        self.write_line("  -----------------------------------------------------------------------------")

        field_offset = 0
        for field in temp_obj.get(KEY_FIELDS_DEF, []):
            l = self._dump_field(field_offset, field)
            field_offset += l

        self.write_line("  -----------------------------------------------------------------------------")
        self.write_line("  Calc Length    : ", field_offset)
        self.write_line("")
        self.write_line("")
        self.write_line("")
        self.write_line("")

    def _dump_field(self, field_offset, field):
        field_id = field[FLD_ID]
        try:
            ent_id = str(field[FLD_ENT_NUM])
            field_id |= FLD_END_E_MASK
        except KeyError:
            ent_id = ""

        self.write_line("  | %-40s|%6d |%7s |%7d |%6d |" %
                        (field[FLD_NAME], field_id, ent_id, field_offset, field[FLD_LEN]))
        return field[FLD_LEN]