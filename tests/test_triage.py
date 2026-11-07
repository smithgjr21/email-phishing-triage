import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from email_triage import inspect
class EmailTests(unittest.TestCase):
 def test_sample(self):
  report=inspect(Path(__file__).resolve().parents[1]/'samples/training_message.eml')
  self.assertEqual(report['subject'],'Training sample - account review')
  self.assertEqual(len(report['urls']),1)
  self.assertTrue(report['review_indicators'])
if __name__=='__main__':unittest.main()
