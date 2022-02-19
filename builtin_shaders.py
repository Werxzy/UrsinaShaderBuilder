Base_Shader = {
	'version': '0.0',
	'nodes': {
		'fragment': {
			'node_0': {
				'class': 'ConstantNode',
				'position': [-0.9878981709480286, -0.14414763450622559],
				'input connections': [],
				'data type': 'vec3',
				'values': ['1', '1', '1']
			},
			'node_1': {
				'class': 'UserInOutNode',
				'position': [-1.0227763652801514, -0.013417009264230728],
				'input connections': [],
				'name': 'normal',
				'data type': 'vec3',
				'is output': True,
				'uniform': 'False'
			},
			'node_2': {
				'class': 'InstructionNode',
				'position': [-0.6632858514785767, -0.14404667913913727],
				'input connections': ['node_0.0'],
				'instruction': 'Normalize'
				},
			'node_3': {
				'class': 'InstructionNode',
				'position': [-0.6648553013801575, -0.013185500167310238],
				'input connections': ['node_1.0'],
				'instruction': 'Normalize'
			},
			'node_4': {
				'class': 'ConstantNode',
				'position': [-0.2572380304336548, -0.2464004009962082],
				'input connections': [],
				'data type': 'float',
				'values': ['1']
			},
			'node_5': {
				'class': 'ConstantNode',
				'position': [-0.2586352229118347, -0.15604223310947418],
				'input connections': [],
				'data type': 'float',
				'values': ['0.2']
			},
			'node_6': {
				'class': 'InstructionNode',
				'position': [-0.2745814323425293, -0.013428960926830769],
				'input connections': ['node_3.0', 'node_2.0'],
				'instruction': 'Dot Product'
			},
			'node_7': {
				'class': 'InstructionNode',
				'position': [0.1928420215845108, -0.013236058875918388],
				'input connections': ['node_6.0', 'node_5.0', 'node_4.0'],
				'instruction': 'Clamp'
			},
			'node_8': {
				'class': 'ConstantNode',
				'position': [0.23759688436985016, 0.15249699354171753],
				'input connections': [],
				'data type': 'vec3',
				'values': ['1.0', '0.3', '0.2']
			},
			'node_9': {
				'class': 'ConstantNode',
				'position': [0.6029052734375, -0.10627293586730957],
				'input connections': [],
				'data type': 'float',
				'values': ['1']
			},
			'node_10': {
				'class': 'InstructionNode',
				'position': [0.6037036180496216, 0.02303239516913891],
				'input connections': ['node_8.0', 'node_7.0'],
				'instruction': 'Multiply'
			},
			'node_11': {
				'class': 'UserInOutNode',
				'position': [0.551273763179779, 0.23542802035808563],
				'input connections': [],
				'name': 'uv',
				'data type': 'vec2',
				'is output': True,
				'uniform': 'False'
			},
				'node_12': {
				'class': 'BuiltInOutputNode',
				'position': [0.48888927698135376, 0.28890034556388855],
				'input connections': [],
				'variable': 'p3d_Texture0'
			},
			'node_17': {
				'class': 'ConvertNode',
				'position': [0.9884258508682251, 0.023148179054260254],
				'input connections': ['node_10.0', 'node_9.0'],
				'from data type': 'vec3',
				'to data type': 'vec4'
			},
			'node_18': {
				'class': 'InstructionNode',
				'position': [0.9854183197021484, 0.29908645153045654],
				'input connections': ['node_12.0', 'node_11.0'],
				'instruction': 'Texture Sample'
			},
			'node_22': {
				'class': 'InstructionNode',
				'position': [1.3508110046386719, 0.053368061780929565],
				'input connections': ['node_18.0', 'node_17.0'],
				'instruction': 'Multiply'
			},
			'node_26': {
				'class': 'BuiltInOutputNode',
				'position': [1.7379523515701294, 0.045393720269203186],
				'input connections': ['node_22.0'],
				'variable': 'p3d_FragColor'
			}
		},
		'vertex': {
			'node_13': {
				'class': 'BuiltInOutputNode',
				'position': [-0.325813353061676, -0.0011574334930628538],
				'input connections': [],
				'variable': 'p3d_Normal'
			},
			'node_14': {
				'class': 'BuiltInOutputNode',
				'position': [-0.3309316337108612, 0.054234616458415985],
				'input connections': [],
				'variable': 'p3d_NormalMatrix'
			},
			'node_15': {
				'class': 'BuiltInOutputNode',
				'position': [-0.3185187876224518, 0.17488424479961395],
				'input connections': [],
				'variable': 'p3d_Vertex'
			},
			'node_16': {
				'class': 'BuiltInOutputNode',
				'position': [-0.37962934374809265, 0.22800925374031067],
				'input connections': [],
				'variable': 'p3d_ModelViewProjectionMatrix'
			},
			'node_19': {
				'class': 'InstructionNode',
				'position': [0.06076404079794884, 0.06458339095115662],
				'input connections': ['node_14.0', 'node_13.0'],
				'instruction': 'Multiply'
			},
			'node_20': {
				'class': 'InstructionNode',
				'position': [0.05960652604699135, 0.23888884484767914],
				'input connections': ['node_16.0', 'node_15.0'],
				'instruction': 'Multiply'
			},
			'node_21': {
				'class': 'BuiltInOutputNode',
				'position': [0.057291850447654724, -0.11596069484949112],
				'input connections': [],
				'variable': 'p3d_MultiTexCoord0'
			},
			'node_23': {
				'class': 'UserInOutNode',
				'position': [0.45266252756118774, 0.06423623859882355],
				'input connections': ['node_19.0'],
				'name': 'normal',
				'data type': 'vec3',
				'is output': False
			},
			'node_24': {
				'class': 'BuiltInOutputNode',
				'position': [0.45543980598449707, 0.22534717619419098],
				'input connections': ['node_20.0'],
				'variable': 'gl_Position'
			},
			'node_25': {
				'class': 'UserInOutNode',
				'position': [0.4405093193054199, -0.10450232028961182],
				'input connections': ['node_21.0'],
				'name': 'uv',
				'data type': 'vec2',
				'is output': False
			}
		}
	}
}