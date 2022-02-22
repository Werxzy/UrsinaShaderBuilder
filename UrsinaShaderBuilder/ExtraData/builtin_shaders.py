Base_Shader = {
    "version": "0.0",
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
