Base_Shader = {
    "version": "0.1.0",
    "nodes": {
        "fragment": {
            "node_0": {
                "class": "ConstantNode",
                "position": [-0.9298228621482849, -0.14107942581176758],
                "input connections": [],
                "data type": "vec3",
                "values": ["1", "1", "-1"]
            },
            "node_1": {
                "class": "UserInOutNode",
                "position": [-0.9602762460708618, -0.008787397295236588],
                "input connections": [],
                "name": "normal",
                "data type": "vec3",
                "is output": True,
                "uniform": "false"
            },
            "node_2": {
                "class": "InstructionNode",
                "position": [-0.6019435524940491, -0.1417318731546402],
                "input connections": ["node_0.0"],
                "instruction": "Normalize"
            },
            "node_3": {
                "class": "InstructionNode",
                "position": [-0.6011977195739746, -0.009713291190564632],
                "input connections": ["node_1.0"],
                "instruction": "Normalize"
            },
            "node_4": {
                "class": "ConstantNode",
                "position": [-0.19266295433044434, -0.14099593460559845],
                "input connections": [],
                "data type": "float",
                "values": ["0.2"]
            },
            "node_5": {
                "class": "InstructionNode",
                "position": [-0.20397958159446716, -0.009956751950085163],
                "input connections": ["node_3.0", "node_2.0"],
                "instruction": "Dot Product"
            },
            "node_6": {
                "class": "InstructionNode",
                "position": [0.20138905942440033, -0.009259134531021118],
                "input connections": ["node_5.0", "node_4.0"],
                "instruction": "Maximum"
            },
            "node_7": {
                "class": "ConstantNode",
                "position": [0.2267172932624817, 0.16846919059753418],
                "input connections": [],
                "data type": "vec3",
                "values": ["1.0", "0.95", "0.9"]
            },
            "node_9": {
                "class": "ConstantNode",
                "position": [0.6029052734375, -0.10627293586730957],
                "input connections": [],
                "data type": "float",
                "values": ["1"]
            },
            "node_10": {
                "class": "InstructionNode",
                "position": [0.6037036180496216, 0.02303239516913891],
                "input connections": ["node_7.0", "node_6.0"],
                "instruction": "Multiply"
            },
            "node_11": {
                "class": "UserInOutNode",
                "position": [0.551273763179779, 0.23542802035808563],
                "input connections": [],
                "name": "uv",
                "data type": "vec2",
                "is output": True,
                "uniform": "false"
            },
            "node_12": {
                "class": "BuiltInOutputNode",
                "position": [0.48888927698135376, 0.28890034556388855],
                "input connections": [],
                "variable": "p3d_Texture0"
            },
            "node_17": {
                "class": "ConvertNode",
                "position": [0.9884258508682251, 0.023148179054260254],
                "input connections": ["node_10.0", "node_9.0"],
                "from data type": "vec3",
                "to data type": "vec4"
            },
            "node_18": {
                "class": "InstructionNode",
                "position": [0.9854183197021484, 0.29908645153045654],
                "input connections": ["node_12.0", "node_11.0"],
                "instruction": "Texture Sample"
            },
            "node_22": {
                "class": "InstructionNode",
                "position": [1.3508110046386719, 0.053368061780929565],
                "input connections": ["node_18.0", "node_17.0"],
                "instruction": "Multiply"
            },
            "node_30": {
                "class": "BuiltInOutputNode",
                "position": [1.7379523515701294, 0.045393720269203186],
                "input connections": ["node_22.0"],
                "variable": "p3d_FragColor"
            },
            "node_31": {
                "class": "CommentNode",
                "position": [-0.01933959499001503, -0.23709402978420258],
                "input connections": [],
                "text": "The dot product of the normal and light direciton gives \na lightness value.\n\ngetting the maximum of the dot product and 0.2 ensures\nthat the back isn't completely dark.\n\nThe vec3 with (1.0,0.95,0.9) acts as the light's color.",
                "size": [0.6672455871754317, 0.14456015961174956]
            },
            "node_32": {
                "class": "CommentNode",
                "position": [0.9965274333953857, -0.10648176074028015],
                "input connections": [],
                "text": "This convert node adds a \n1 to the vec3 to apply a\ntransparency value.",
                "size": [0.288773355019102, 0.1]
            },
            "node_33": {
                "class": "CommentNode",
                "position": [1.973418116569519, 0.10074605792760849],
                "input connections": [],
                "text": "Final pixel color",
                "size": [0.21006964027750114, 0.1]
            }
        },
        "vertex": {
            "node_8": {
                "class": "BuiltInOutputNode",
                "position": [-0.6909725069999695, 0.05555561184883118],
                "input connections": [],
                "variable": "p3d_ModelMatrix"
            },
            "node_13": {
                "class": "BuiltInOutputNode",
                "position": [-0.29572099447250366, -0.065972238779068],
                "input connections": [],
                "variable": "p3d_Normal"
            },
            "node_14": {
                "class": "ConvertNode",
                "position": [-0.2951388955116272, 0.06597232818603516],
                "input connections": ["node_8.0"],
                "from data type": "mat4",
                "to data type": "mat3"
            },
            "node_15": {
                "class": "BuiltInOutputNode",
                "position": [-0.3185187876224518, 0.17488424479961395],
                "input connections": [],
                "variable": "p3d_Vertex"
            },
            "node_16": {
                "class": "BuiltInOutputNode",
                "position": [-0.37962934374809265, 0.22800925374031067],
                "input connections": [],
                "variable": "p3d_ModelViewProjectionMatrix"
            },
            "node_19": {
                "class": "InstructionNode",
                "position": [0.06076404079794884, 0.06458339095115662],
                "input connections": ["node_14.0", "node_13.0"],
                "instruction": "Multiply"
            },
            "node_20": {
                "class": "InstructionNode",
                "position": [0.05960652604699135, 0.23888884484767914],
                "input connections": ["node_16.0", "node_15.0"],
                "instruction": "Multiply"
            },
            "node_21": {
                "class": "BuiltInOutputNode",
                "position": [0.057291850447654724, -0.11596069484949112],
                "input connections": [],
                "variable": "p3d_MultiTexCoord0"
            },
            "node_23": {
                "class": "UserInOutNode",
                "position": [0.4434036612510681, 0.06423626840114594],
                "input connections": ["node_19.0"],
                "name": "normal",
                "data type": "vec3",
                "is output": False
            },
            "node_24": {
                "class": "BuiltInOutputNode",
                "position": [0.45543980598449707, 0.22534717619419098],
                "input connections": ["node_20.0"],
                "variable": "gl_Position"
            },
            "node_25": {
                "class": "UserInOutNode",
                "position": [0.4405093193054199, -0.10450232028961182],
                "input connections": ["node_21.0"],
                "name": "uv",
                "data type": "vec2",
                "is output": False
            },
            "node_26": {
                "class": "CommentNode",
                "position": [-0.2686818242073059, -0.1285364031791687],
                "input connections": [],
                "text": "The default sphere\nhas flat faces.",
                "size": [0.21932897349067149, 0.1]
            },
            "node_27": {
                "class": "CommentNode",
                "position": [-0.6813279986381531, 0.002134948968887329],
                "input connections": [],
                "text": "Use ModelMatrix\ninstead of\nNormalMatrix.",
                "size": [0.2, 0.1]
            },
            "node_28": {
                "class": "CommentNode",
                "position": [0.7272941470146179, 0.2943802773952484],
                "input connections": [],
                "text": "These nodes on the top \nrow are almost always \nincluded.",
                "size": [0.2644677597271166, 0.1]
            },
            "node_29": {
                "class": "CommentNode",
                "position": [0.6979547142982483, -0.059207767248153687],
                "input connections": [],
                "text": "Transfering of\nthe texture\ncoordinates.",
                "size": [0.2, 0.1]
            }
        }
    },
}

Curve_Shader = {
    'version': '0.1.1',
    'nodes': {
        'vertex': {
            'node_0': {
                'class': 'BuiltInOutputNode',
                'position': [-2.502855062484741, 0.5012853741645813],
                'input connections': [],
                'variable': 'p3d_Vertex'
            },
            'node_1': {
                'class': 'ConstantNode',
                'position': [-2.0008420944213867, 1.2756401300430298],
                'input connections': [],
                'data type': 'float',
                'values': ['3.0']
            },
            'node_2': {
                'class': 'UserInOutNode',
                'position': [-2.030667781829834, 1.4087196588516235],
                'input connections': [],
                'name': 'C1',
                'data type': 'vec2',
                'is output': True,
                'uniform': 'True'
            },
            'node_3': {
                'class': 'ConstantNode',
                'position': [-2.006434440612793, 1.055686116218567],
                'input connections': [],
                'data type': 'float',
                'values': ['2.0']
            },
            'node_4': {
                'class': 'UserInOutNode',
                'position': [-2.032923698425293, 1.1938358545303345],
                'input connections': [],
                'name': 'C2',
                'data type': 'vec2',
                'is output': True,
                'uniform': 'True'
            },
            'node_5': {
                'class': 'VariableSplitterNode',
                'position': [-2.0819153785705566, 0.515765368938446],
                'input connections': ['node_0.0'],
                'data type': 'vec4',
                'merge': 'False'
            },
            'node_6': {
                'class': 'InstructionNode',
                'position': [-1.6746398210525513, 1.407984972000122],
                'input connections': ['node_2.0', 'node_1.0'],
                'instruction': 'Multiply'
            },
            'node_7': {
                'class': 'InstructionNode',
                'position': [-1.6765042543411255, 1.1936230659484863],
                'input connections': ['node_4.0', 'node_3.0'],
                'instruction': 'Multiply'
            },
            'node_8': {
                'class': 'InstructionNode',
                'position': [-1.2925153970718384, 1.409848690032959],
                'input connections': ['node_6.0', 'node_5.0'],
                'instruction': 'Multiply'
            },
            'node_9': {
                'class': 'InstructionNode',
                'position': [-1.0464657545089722, 1.2234474420547485],
                'input connections': ['node_8.0', 'node_7.0'],
                'instruction': 'Add'
            },
            'node_10': {
                'class': 'UserInOutNode',
                'position': [-2.0872936248779297, 0.25085145235061646],
                'input connections': [],
                'name': 'C1',
                'data type': 'vec2',
                'is output': True,
                'uniform': 'True'
            },
            'node_11': {
                'class': 'UserInOutNode',
                'position': [-0.7377309799194336, 1.0782270431518555],
                'input connections': [],
                'name': 'C3',
                'data type': 'vec2',
                'is output': True,
                'uniform': 'True'
            },
            'node_12': {
                'class': 'InstructionNode',
                'position': [-0.6791832447052002, 1.2264512777328491],
                'input connections': ['node_9.0', 'node_5.0'],
                'instruction': 'Multiply'
            },
            'node_13': {
                'class': 'UserInOutNode',
                'position': [-1.7525120973587036, 0.12560255825519562],
                'input connections': [],
                'name': 'C2',
                'data type': 'vec2',
                'is output': True,
                'uniform': 'True'
            },
            'node_14': {
                'class': 'InstructionNode',
                'position': [-1.7268301248550415, 0.28025567531585693],
                'input connections': ['node_5.0', 'node_10.0'],
                'instruction': 'Multiply'
            },
            'node_15': {
                'class': 'InstructionNode',
                'position': [-0.3120431900024414, 1.2290364503860474],
                'input connections': ['node_12.0', 'node_11.0'],
                'instruction': 'Add'
            },
            'node_16': {
                'class': 'InstructionNode',
                'position': [-1.3838530778884888, 0.15536700189113617],
                'input connections': ['node_14.0', 'node_13.0'],
                'instruction': 'Add'
            },
            'node_17': {
                'class': 'ConstantNode',
                'position': [0.0946657583117485, 1.1113120317459106],
                'input connections': [],
                'data type': 'float',
                'values': ['-1']
            },
            'node_18': {
                'class': 'VariableSplitterNode',
                'position': [0.09652990847826004, 1.2343392372131348],
                'input connections': ['node_15.0'],
                'data type': 'vec2',
                'merge': 'False'
            },
            'node_19': {
                'class': 'UserInOutNode',
                'position': [-1.052125334739685, 0.13891838490962982],
                'input connections': [],
                'name': 'C3',
                'data type': 'vec2',
                'is output': True,
                'uniform': 'True'
            },
            'node_20': {
                'class': 'InstructionNode',
                'position': [-1.0557860136032104, 0.28771188855171204],
                'input connections': ['node_5.0', 'node_16.0'],
                'instruction': 'Multiply'
            },
            'node_21': {
                'class': 'InstructionNode',
                'position': [0.4320528507232666, 1.2045153379440308],
                'input connections': ['node_18.1', 'node_17.0'],
                'instruction': 'Multiply'
            },
            'node_22': {
                'class': 'InstructionNode',
                'position': [-0.6885746121406555, 0.16841478645801544],
                'input connections': ['node_20.0', 'node_19.0'],
                'instruction': 'Add'
            },
            'node_23': {
                'class': 'UserInOutNode',
                'position': [-0.6136605143547058, 0.7161433696746826],
                'input connections': [],
                'name': 'thickness',
                'data type': 'float',
                'is output': True,
                'uniform': 'True'
            },
            'node_24': {
                'class': 'VariableSplitterNode',
                'position': [0.8160396814346313, 1.2716187238693237],
                'input connections': ['node_21.0', 'node_18.0'],
                'data type': 'vec2',
                'merge': 'True'
            },
            'node_25': {
                'class': 'UserInOutNode',
                'position': [-0.35954171419143677, 0.13872130215168],
                'input connections': [],
                'name': 'C4',
                'data type': 'vec2',
                'is output': True,
                'uniform': 'True'
            },
            'node_26': {
                'class': 'InstructionNode',
                'position': [-0.3641635775566101, 0.2963079512119293],
                'input connections': ['node_5.0', 'node_22.0'],
                'instruction': 'Multiply'
            },
            'node_27': {
                'class': 'InstructionNode',
                'position': [-0.223512202501297, 0.5872273445129395],
                'input connections': ['node_23.0', 'node_5.1'],
                'instruction': 'Multiply'
            },
            'node_28': {
                'class': 'InstructionNode',
                'position': [-0.22967270016670227, 0.7198702096939087],
                'input connections': ['node_24.0'],
                'instruction': 'Normalize'
            },
            'node_29': {
                'class': 'InstructionNode',
                'position': [-0.004408824723213911, 0.16955465078353882],
                'input connections': ['node_26.0', 'node_25.0'],
                'instruction': 'Add'
            },
            'node_30': {
                'class': 'InstructionNode',
                'position': [0.1394023895263672, 0.7198705077171326],
                'input connections': ['node_28.0', 'node_27.0'],
                'instruction': 'Multiply'
            },
            'node_33': {
                'class': 'ConstantNode',
                'position': [0.29347819089889526, 0.04396898299455643],
                'input connections': [],
                'data type': 'float',
                'values': ['1']
            },
            'node_34': {
                'class': 'InstructionNode',
                'position': [0.33512377738952637, 0.4458596110343933],
                'input connections': ['node_30.0', 'node_29.0'],
                'instruction': 'Add'
            },
            'node_37': {
                'class': 'ConvertNode',
                'position': [0.782657265663147, 0.2550927698612213],
                'input connections': ['node_34.0', 'disconnected', 'node_33.0'],
                'from data type': 'vec2',
                'to data type': 'vec4'
            },
            'node_38': {
                'class': 'BuiltInOutputNode',
                'position': [0.6439017057418823, 0.508309006690979],
                'input connections': [],
                'variable': 'p3d_ModelViewProjectionMatrix'
            },
            'node_40': {
                'class': 'BuiltInOutputNode',
                'position': [0.057291850447654724, -0.11596069484949112],
                'input connections': [],
                'variable': 'p3d_MultiTexCoord0'
            },
            'node_41': {
                'class': 'InstructionNode',
                'position': [1.0986961126327515, 0.49519994854927063],
                'input connections': ['node_38.0', 'node_37.0'],
                'instruction': 'Multiply'
            },
            'node_43': {
                'class': 'CommentNode',
                'position': [0.6979547142982483, -0.059207767248153687],
                'input connections': [],
                'text': 'Transfering of\nthe texture\ncoordinates.',
                'size': [0.2, 0.1]
            },
            'node_44': {
                'class': 'UserInOutNode',
                'position': [0.4405093193054199, -0.10450232028961182],
                'input connections': ['node_40.0'],
                'name': 'uv',
                'data type': 'vec2',
                'is output': False
            },
            'node_45': {
                'class': 'BuiltInOutputNode',
                'position': [1.528923749923706, 0.39671674370765686],
                'input connections': ['node_41.0'],
                'variable': 'gl_Position'
            }
        },
        'fragment': {
            'node_31': {
                'class': 'UserInOutNode',
                'position': [0.23148125410079956, 0.025462985038757324],
                'input connections': [],
                'name': 'uv',
                'data type': 'vec2',
                'is output': True,
                'uniform': 'False'
            },
            'node_32': {
                'class': 'BuiltInOutputNode',
                'position': [0.17245317995548248, 0.07986113429069519],
                'input connections': [],
                'variable': 'p3d_Texture0'
            },
            'node_35': {
                'class': 'InstructionNode',
                'position': [0.6712950468063354, 0.090277761220932],
                'input connections': ['node_32.0', 'node_31.0'],
                'instruction': 'Texture Sample'
            },
            'node_36': {
                'class': 'BuiltInOutputNode',
                'position': [0.7012477517127991, 0.15323008596897125],
                'input connections': [],
                'variable': 'p3d_ColorScale'
            },
            'node_39': {
                'class': 'InstructionNode',
                'position': [1.0685573816299438, 0.16375195980072021],
                'input connections': ['node_36.0', 'node_35.0'],
                'instruction': 'Multiply'
            },
            'node_42': {
                'class': 'BuiltInOutputNode',
                'position': [1.466774821281433, 0.1528126448392868],
                'input connections': ['node_39.0'],
                'variable': 'p3d_FragColor'
            }
        }
    },
    'vertex': '#version 450\n\nin vec4 p3d_Vertex;\nuniform vec2 C1;\nuniform vec2 C2;\nuniform vec2 C3;\nuniform float thickness;\nuniform vec2 C4;\nuniform mat4 p3d_ModelViewProjectionMatrix;\nin vec2 p3d_MultiTexCoord0;\nout vec2 uv;\nout vec4 gl_Position;\n\nvoid main(){\nfloat _float_0 = p3d_Vertex.x;\nfloat _float_1 = p3d_Vertex.y;\nvec2 _vec2_0=C1*3.0;\nvec2 _vec2_1=C2*2.0;\n_vec2_0=_vec2_0*_float_0;\n_vec2_1=_vec2_0+_vec2_1;\n_vec2_1=_vec2_1*_float_0;\n_vec2_0=_float_0*C1;\n_vec2_1=_vec2_1+C3;\n_vec2_0=_vec2_0+C2;\nfloat _float_2 = _vec2_1.x;\nfloat _float_3 = _vec2_1.y;\n_vec2_0=_float_0*_vec2_0;\n_float_3=_float_3*-1;\n_vec2_0=_vec2_0+C3;\n_vec2_1 = vec2(_float_3,_float_2);\n_vec2_0=_float_0*_vec2_0;\n_float_1=thickness*_float_1;\n_vec2_1=normalize(_vec2_1);\n_vec2_0=_vec2_0+C4;\n_vec2_1=_vec2_1*_float_1;\n_vec2_0=_vec2_1+_vec2_0;\nvec4 _vec4_0 = vec4(_vec2_0,0,1);\n_vec4_0=p3d_ModelViewProjectionMatrix*_vec4_0;\nuv = p3d_MultiTexCoord0;\ngl_Position = _vec4_0;\n}',
    'fragment': '#version 450\n\nin vec2 uv;\nuniform sampler2D p3d_Texture0;\nuniform vec4 p3d_ColorScale;\nout vec4 p3d_FragColor;\n\nvoid main(){\nvec4 _vec4_0=texture(p3d_Texture0,uv);\n_vec4_0=p3d_ColorScale*_vec4_0;\np3d_FragColor = _vec4_0;\n}'
}


Box_Shader = {
    "vertex": "#version 450\n\nuniform vec4[128] scales;\nin vec4 p3d_Vertex;\nuniform vec4[128] positions;\nuniform vec4[128] colors;\nuniform mat4 p3d_ModelViewProjectionMatrix;\nout vec4 color;\nout vec4 gl_Position;\n\nvoid main(){\nvec4[128] _vec4_array_128_2 = colors;\nvec4[128] _vec4_array_128_1 = positions;\nvec4[128] _vec4_array_128_0 = scales;\nvec4 _vec4_0 = _vec4_array_128_0[gl_InstanceID];\nvec2 _vec2_0 = vec2(_vec4_0.xy);\nfloat _float_0 = _vec4_0.z;\nfloat _float_1 = _vec4_0.w;\nvec2 _vec2_1 = vec2(p3d_Vertex.xy);\nfloat _float_2 = p3d_Vertex.z;\nfloat _float_3 = p3d_Vertex.w;\nvec2 _vec2_2 = vec2(_float_0,_float_1);\nvec2 _vec2_3=sign(_vec2_1);\n_vec2_1=_vec2_2*_vec2_1;\n_vec2_3=_vec2_0*_vec2_3;\n_vec2_1=_vec2_3+_vec2_1;\n_vec4_0 = vec4(_vec2_1,_float_2,_float_3);\nvec4 _vec4_1 = _vec4_array_128_1[gl_InstanceID];\n_vec4_0=_vec4_1+_vec4_0;\n_vec4_1 = _vec4_array_128_2[gl_InstanceID];\n_vec4_0=p3d_ModelViewProjectionMatrix*_vec4_0;\ncolor = _vec4_1;\ngl_Position = _vec4_0;\n}",
    "fragment": "#version 450\n\nin vec4 color;\nout vec4 p3d_FragColor;\n\nvoid main(){\np3d_FragColor = color;\n}"
}