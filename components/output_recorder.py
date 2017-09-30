import datetime
import glob
import os.path
import re
if False:
	import util
else:
	import common_util as util
if False:
	from _stubs import *

print('common output_recording.py initializing')

class OutputRecorderExt:
	def __init__(self, comp):
		self.comp = comp
		self.UpdateParamStates()
		self.UpdateFileNameLabel()

	@property
	def BaseFileName(self):
		basename = self.comp.par.Basename.eval()
		if basename:
			return basename
		return os.path.splitext(project.name)[0] + '-output'

	@property
	def NextFileName(self):
		base = self.BaseFileName
		path = self.comp.par.Folder.eval()
		if path:
			base = os.path.join(path.replace('/', os.path.sep), base)
		base += '-' + str(datetime.date.today()) + '-'
		files = glob.glob(base + '*')
		if len(files) == 0:
			i = 1
		else:
			i = max([_getIndex(base, f) for f in files]) + 1
		# print(self.comp.path + '--ZZZ base: {!r} considering files: {!r}, next index: {}'.format(base, files, i))
		# for _F in files:
		# 	print('  [{}]: {}'.format(_F, _getIndex(base, _F)))
		return base.replace(os.path.sep, '/') + str(i) + self._FileNameSuffix

	@property
	def _ResolutionSuffix(self):
		if self.comp.par.Useinputres:
			video = self.comp.op('./video')
			w, h = video.width, video.height
		else:
			w, h = self.comp.par.Resolution1.eval(), self.comp.par.Resolution2.eval()
		return '{}x{}'.format(w, h)

	@property
	def _VideoCodecSuffix(self):
		vcodec = self.comp.par.Videocodec.eval()
		suffix = self.comp.op('./video_codecs')[vcodec, 'suffix']
		return suffix.val if suffix and suffix.val else vcodec

	@property
	def _FileNameSuffix(self):
		parts = []
		if self.comp.par.Suffix:
			parts.append(self.comp.par.Suffix.eval())
		if self.comp.par.Addvcodecsfx:
			parts.append(self._VideoCodecSuffix)
		if self.comp.par.Addacodecsfx:
			parts.append(self.comp.par.Audiocodec.eval())
		if self.comp.par.Addresolutionsfx:
			parts.append(self._ResolutionSuffix)
		return ('-' + '-'.join(parts)) if parts else ''

	@property
	def NextFileFullPath(self):
		return self.NextFileName

	def CaptureImage(self):
		f = self.NextFileFullPath + '.' + self.comp.par.Imageext
		print('saving image ' + f)
		self.comp.op('video').save(f)
		ui.status = 'saved image ' + f
		self.UpdateFileNameLabel()

	def StartVideoCapture(self):
		f = self.NextFileFullPath + '.' + self.comp.par.Videoext
		m = self.comp.op('moviefileout')
		print('starting video recording ' + f)
		m.par.file = f
		m.par.record = 1
		self.UpdateFileNameLabel()

	def EndVideoCapture(self):
		m = self.comp.op('moviefileout')
		f = m.par.file
		print('finished video recording ' + f)
		ui.status = 'saved video ' + f
		m.par.record = 0
		self.UpdateFileNameLabel()

	def UpdateFileNameLabel(self):
		self.comp.op('nextfilename_value').par.Label = self.NextFileName

	def UpdateParamStates(self):
		useinput = self.comp.par.Useinputres.eval()
		self.comp.par.Resolution1.enable = not useinput
		self.comp.par.Resolution2.enable = not useinput

	def UpdateHeight(self):
		if self.comp.par.Autoheight:
			self.comp.par.h = max(util.GetVisibleChildCOMPsHeight(self.comp.op('root_panel')), 20)

def _getIndex(base, f):
	if not f.startswith(base):
		return 0
	f = f[len(base):]
	r = re.match(r'([0-9]+)[^0-9]+', f)
	return int(r.group(1)) if r else 0

