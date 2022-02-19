Base_Shader = {
    'version': '0.0',
    'nodes': {
        'fragment': {
            'node_0': {
                'class': 'ConstantNode',
                'position': [-0.9298228621482849, -0.14107942581176758],
                'input connections': [],
                'data type': 'vec3',
                'values': ['1', '1', '-1']
            },
            'node_1': {
                'class': 'UserInOutNode',
                'position': [-0.9602762460708618, -0.008787397295236588],
                'input connections': [],
                'name': 'normal',
                'data type': 'vec3',
                'is output': True,
                'uniform': 'False'
            },
            'node_2': {
                'class': 'InstructionNode',
                'position': [-0.6019435524940491, -0.1417318731546402],
                'input connections': ['node_0.0'],
                'instruction': 'Normalize'
            },
            'node_3': {
                'class': 'InstructionNode',
                'position': [-0.6011977195739746, -0.009713291190564632],
                'input connections': ['node_1.0'],
                'instruction': 'Normalize'
            },
            'node_4': {
                'class': 'ConstantNode',
                'position': [-0.19266295433044434, -0.14099593460559845],
                'input connections': [],
                'data type': 'float',
                'values': ['0.2']
            },
            'node_5': {
                'class': 'InstructionNode',
                'position': [-0.20397958159446716, -0.009956751950085163],
                'input connections': ['node_3.0', 'node_2.0'],
                'instruction': 'Dot Product'
            },
            'node_7': {
                'class': 'InstructionNode',
                'position': [0.20138905942440033, -0.009259134531021118],
                'input connections': ['node_5.0', 'node_4.0'],
                'instruction': 'Maximum'
            },
            'node_8': {
                'class': 'ConstantNode',
                'position': [0.2318098545074463, 0.17101550102233887],
                'input connections': [],
                'data type': 'vec3',
                'values': ['1.0', '0.3', '0.2']
            },
            'node_11': {
                'class': 'ConstantNode',
                'position': [0.6029052734375, -0.10627293586730957],
                'input connections': [],
                'data type': 'float',
                'values': ['1']
            },
            'node_12': {
                'class': 'InstructionNode',
                'position': [0.6037036180496216, 0.02303239516913891],
                'input connections': ['node_8.0', 'node_7.0'],
                'instruction': 'Multiply'
            },
            'node_13': {
                'class': 'UserInOutNode',
                'position': [0.551273763179779, 0.23542802035808563],
                'input connections': [],
                'name': 'uv',
                'data type': 'vec2',
                'is output': True,
                'uniform': 'False'
            },
            'node_14': {
                'class': 'BuiltInOutputNode',
                'position': [0.48888927698135376, 0.28890034556388855],
                'input connections': [],
                'variable': 'p3d_Texture0'
            },
            'node_18': {
                'class': 'ConvertNode',
                'position': [0.9884258508682251, 0.023148179054260254],
                'input connections': ['node_12.0', 'node_11.0'],
                'from data type': 'vec3',
                'to data type': 'vec4'
            },
            'node_19': {
                'class': 'InstructionNode',
                'position': [0.9854183197021484, 0.29908645153045654],
                'input connections': ['node_14.0', 'node_13.0'],
                'instruction': 'Texture Sample'
            },
            'node_23': {
                'class': 'InstructionNode',
                'position': [1.3508110046386719, 0.053368061780929565],
                'input connections': ['node_19.0', 'node_18.0'],
                'instruction': 'Multiply'
            },
            'node_27': {
                'class': 'BuiltInOutputNode',
                'position': [1.7379523515701294, 0.045393720269203186],
                'input connections': ['node_23.0'],
                'variable': 'p3d_FragColor'
            }
        },
        'vertex': {
            'node_6': {
                'class': 'BuiltInOutputNode',
                'position': [-0.6857671737670898, -0.011574119329452515],
                'input connections': [],
                'variable': 'p3d_Normal'
            },
            'node_9': {
                'class': 'ConvertNode',
                'position': [-0.3009258210659027, -0.0011572837829589844],
                'input connections': ['node_6.0', 'disconnected'],
                'from data type': 'vec3',
                'to data type': 'vec4'
            },
            'node_10': {
                'class': 'BuiltInOutputNode',
                'position': [-0.31134241819381714, 0.05439820885658264],
                'input connections': [],
                'variable': 'p3d_ModelMatrix'
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
            'node_17': {
                'class': 'InstructionNode',
                'position': [0.06076404079794884, 0.06458339095115662],
                'input connections': ['node_10.0', 'node_9.0'],
                'instruction': 'Multiply'
            },
            'node_20': {
                'class': 'BuiltInOutputNode',
                'position': [0.057291850447654724, -0.11596069484949112],
                'input connections': [],
                'variable': 'p3d_MultiTexCoord0'
            },
            'node_21': {
                'class': 'InstructionNode',
                'position': [0.05960652604699135, 0.23888884484767914],
                'input connections': ['node_16.0', 'node_15.0'],
                'instruction': 'Multiply'
            },
            'node_22': {
                'class': 'ConvertNode',
                'position': [0.44560185074806213, 0.06597232818603516],
                'input connections': ['node_17.0'],
                'from data type': 'vec4',
                'to data type': 'vec3'
            },
            'node_24': {
                'class': 'UserInOutNode',
                'position': [0.4405093193054199, -0.10450232028961182],
                'input connections': ['node_20.0'],
                'name': 'uv',
                'data type': 'vec2',
                'is output': False
            },
            'node_25': {
                'class': 'BuiltInOutputNode',
                'position': [0.45543980598449707, 0.22534717619419098],
                'input connections': ['node_21.0'],
                'variable': 'gl_Position'
            },
            'node_26': {
                'class': 'UserInOutNode',
                'position': [0.8322924375534058, 0.06539367139339447],
                'input connections': ['node_22.0'],
                'name': 'normal',
                'data type': 'vec3',
                'is output': False
            }
        }
    },
}
