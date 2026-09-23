import unittest
from run import oracle, evolve
from verify import step
import numpy as np

class Semantics(unittest.TestCase):
    def test_joint_distinctions(self):
        rows=[{'seed':i,'base':0,'features':i,'target':(i&1)^((i>>1)&1)} for i in range(4)]
        self.assertIsNotNone(oracle(rows,1)); self.assertIsNotNone(oracle(rows,2))
        self.assertIsNone(oracle(rows,3))
    def test_base_can_distinguish(self):
        rows=[{'seed':0,'base':0,'features':0,'target':0}, {'seed':1,'base':1,'features':0,'target':1}]
        self.assertIsNone(oracle(rows,0))
    def test_first_collision(self):
        rows=[{'seed':i,'base':0,'features':i&1,'target':i//2} for i in range(4)]
        self.assertEqual(oracle(rows,1),[0,2])
    def test_orientation_and_shrinking(self):
        a=np.array([[0,1,1,0,1]],dtype=np.uint8)
        self.assertEqual(evolve(a,170).tolist(),[[1,0,1]])
        self.assertEqual(step(dict(enumerate(a[0].tolist())),170),{1:1,2:0,3:1})

if __name__=='__main__': unittest.main()
