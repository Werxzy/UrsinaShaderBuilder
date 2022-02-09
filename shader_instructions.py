

# this may need to represent in a better way
DataTypes = [
    'bool',
    'int',
    'uint',
    'float',
    'vec2',
    'vec3',
    'vec4',
    'ivec2',
    'ivec3',
    'ivec4',
    'bvec2',
    'bvec3',
    'bvec4',
    'mat2',
    'mat3',
    'mat4',

    'mat2x2',
    'mat2x3',
    'mat2x4',

    'mat3x2',
    'mat3x3',
    'mat3x4',

    'mat4x2',
    'mat4x3',
    'mat4x4',

    'sampler1D',
    'sampler2D',
    'sampler3D',
    'samplerCube',
    'sampler1DShadow',
    'sampler2DShadow',
]

DataMultiTypes = {
    'vec' : ['vec2', 'vec3', 'vec4'],
    'mat' : ['mat2', 'mat3', 'mat4'],
    'ivec' : ['ivec2', 'ivec3', 'ivec4'],
    'uvec' : ['uvec2', 'uvec3', 'uvec4'],
    'bvec' : ['bvec2', 'bvec3', 'bvec4'],
    'genType' : ['float', 'vec2', 'vec3', 'vec4'],
    'intType' : ['int', 'ivec2', 'ivec3', 'ivec4'],
    'uintType' : ['uint', 'uvec2', 'uvec3', 'uvec4'],
    'boolType' : ['bool', 'bvec2', 'bvec3', 'bvec4'],
}
   

# http://mew.cx/glsl_quickref.pdf (bless) (probably outdated and bit unrelated to panda3d)
# https://www.khronos.org/files/opengl-quick-reference-card.pdf (better)

'''
holds all base instructions
'''
# for key, value in GLSL.items: # probably not needed in this way, but just in case

# 1 input and 1 output that are the same type
def simple_func(desc, func, types = ['genType']):
    return {
        'description' : desc, 
        'inputs' : {'a_': list(types)}, 
        'outputs': {'result': list(types)}, 
        'function' : 'result=' + func + '(a_);'
        }

def build_func(desc, func, names = 'abcdef', inputTypes = [['genType'],], outputTypes = ['genType']):
    re = {
        'description' : desc, 
        'inputs' : {}, 
        'outputs': {'result': outputTypes}, 
        'function' : 'result=' + func + '('
        }

    for i in range(len(inputTypes)):
        v = names[i]
        if len(v) == 1:
            v += '_'
        re['inputs'].update({v : inputTypes[i]})
        if i > 0: 
            re['function'] += ','
        re['function'] += v
    
    re['function'] += ');'

    return re


# instructions like swizzle might need special nodes
# how do loops if needed?

'''

be careful with input/output names in the function, as they might replace the incorrect things

'INSTRUCTION NAME' : {
    'description' : '',				# text describing the instruction
    'inputs' : { 					# lists all the inputs and their name
        'INPUT NAME' : ['TYPE'] 	# input name and list of possible types (!!! Nth value in each array is paired together, even in output )
    },
    'outputs' : {					# lists all the outputs and their name (there's almost always only one, but with 'out' there could be multiple)
        'OUTPUT NAME' : ['TYPE']  	# output name and list of possible types
    },
    'function : 'FUNCTION',			# function used to put into GLSL (using str.replace using input names)
}


currently assumes there will be only one of DataMultiTypes in any ith inputs or outputs types
    (there can be genType in all inputs and outputs, but no genType and vec together)

if there's only outputs, there should only be one
    this can be changed, but would need reworking of ShaderNode.update_connections and what GLSL[]['funciton'] stores

'''
GLSL = {

# Arithmatic instructions

    'Add' : {
        'description' : 'Add two values.', 
        'inputs' : {'a': ['genType'],'b': ['genType']}, 
        'outputs': {'result': ['genType']}, 
        'function' : 'result=a+b;'
        },
    'Subtract' : {
        'description' : 'Subtract a value by another.', 
        'inputs' : {'a': ['genType'],'b': ['genType']}, 
        'outputs': {'result': ['genType']}, 
        'function' : 'result=a-b;'
        },
    'Multiply' : {
        'description' : 'Multiply two values.', 
        'inputs' : {'a': ['genType'],'b': ['genType']}, 
        'outputs': {'result': ['genType']}, 
        'function' : 'result=a*b;'
        },
    'Divide' : {
        'description' : 'Divide a value by another.', 
        'inputs' : {'a': ['genType'],'b': ['genType']}, 
        'outputs': {'result': ['genType']}, 
        'function' : 'result=a/b;'
        },
    
# Angle and trigonometry functions

    'Sine' : simple_func('Sine math function.', 'sin'),
    'Cosine' : simple_func('Cosine math function.', 'cos'),
    'Tangent' : simple_func('Tangent math function.', 'tan'),
    'Arc Sine' : simple_func('Arc sine math function.', 'asin'),
    'Arc Cosine' : simple_func('Arc cosine math function.', 'acos'),
    'Arc Tangent' : simple_func('Arc tangent math function.', 'atan'),
    'Arc Tangent 2' : {
        'description' : 'Arc tangent math function using\nseperate x and y inputs.', 
        'inputs' : {'y_': ['genType'], 'x_': ['genType']}, 
        'outputs': {'result': ['genType']}, 
        'function' : 'result=atan(y_,x_);'
        },

    'Hyperbolic Sine' : simple_func('Hyperbolic sine math function.', 'sinh'),
    'Hyperbolic Cosine' : simple_func('Hyperbolic cosine math function.', 'cosh'),
    'Hyperbolic Tangent' : simple_func('Hyperbolic tangent math function.', 'tanh'),
    'Hyperbolic Arc Sine' : simple_func('Hyperbolic arc sine math function.', 'asinh'),
    'Hyperbolic Arc Cosine' : simple_func('Hyperbolic arc cosine math function.', 'acosh'),
    'Hyperbolic Arc Tangent' : simple_func('Hyperbolic arc tangent math function.', 'atanh'),

    'Radians' : simple_func('Converts degrees to radians.', 'radians'),
    'Degrees' : simple_func('Converts radians to degrees.', 'degrees'),
    
# Exponential functions
    
    'Power' : build_func('Math function being a^b.', 'pow', inputTypes=[['genType'], ['genType']]),
    'Exponent' : simple_func('Natural exponential.', 'exp'),
    'Logarithm' : simple_func('Natural logarithm.', 'log'),
    'Exponent 2' : simple_func('Finds 2^return = a', 'exp2'),
    'Logarithm 2' : simple_func('logarithm of 2.', 'log2'),
    'Square Root' : simple_func('Square root.', 'sqrt'),
    'Inverse Square Root' : simple_func('Inverse square root.', 'inversesqrt'),

# Common functions

    'Absolute' : simple_func('Removes the sign of a value.', 'abs', types=['genType', 'intType']),
    'Sign' : simple_func('Gets the sign of a value', 'sign', types=['genType', 'intType']),
    'Ceiling' : simple_func('Rounds the value(s) up.', 'ceil'),
    'Floor' : simple_func('Rounds the value(s) down.', 'floor'),
    'Round' : simple_func('Rounds the value(s)\nto nearest integer.', 'round'),
    'Round Even' : simple_func('Rounds the value(s)\nto nearest even integer.', 'roundEven'),
    'Truncate' : simple_func('Rounds towards zero', 'trunc'),
    'Fraction' : simple_func('Gets the decimal values.', 'frac'),

    'Modulous' : build_func('Gets the remainder of\n dividing by a value.', 'mod', inputTypes=[['genType','genType'], ['genType','float']], outputTypes=['genType','genType']),
    # 'Modf' : { # currently out parameters have no funcitonality in instruction nodes
    #     'description' : 'Seperates decimal from the value.', 
    #     'inputs' : {'a_': ['genType']},
    #     'outputs' : {'integer_': ['genType'], 'decimal_': ['genType']}, 
    #     'function' : 'integer_=modf(a_, out decimal_);'
    # },

    'Maximum' : build_func('Gets the maximum value(s).', 'max', 
        inputTypes=[['genType','genType', 'intType', 'intType', 'uintType', 'uintType'], ['genType','float', 'intType', 'int', 'uintType', 'uint']], 
        outputTypes=['genType','genType', 'intType', 'intType', 'uintType', 'uintType']),
    'Minimum' : build_func('Gets the minimum value(s).', 'min', 
        inputTypes=[['genType','genType', 'intType', 'intType', 'uintType', 'uintType'], ['genType','float', 'intType', 'int', 'uintType', 'uint']], 
        outputTypes=['genType','genType', 'intType', 'intType', 'uintType', 'uintType']),

    'Clamp' : build_func('Clamps a value or vector\nbetween a minimum and maximum.', 'clamp', 
        names=['input_', 'min_', 'max_'],
        inputTypes=[['genType','genType', 'intType', 'intType', 'uintType', 'uintType'], 
                    ['genType','float', 'intType', 'int', 'uintType', 'uint'], 
                    ['genType','float', 'intType', 'int', 'uintType', 'uint']], 
        outputTypes=['genType','genType', 'intType', 'intType', 'uintType', 'uintType']),

    'Interpolate' : build_func('Linearly interpolates between\n two values.', 'mix', names=['from_', 'to_', 'T_'],
        inputTypes=[['genType','genType','genType','genType'], ['genType','genType','genType','genType'], ['genType','float','boolType','bool']], 
        outputTypes=['genType','genType','genType','genType']),

    
    'Smooth Step' : build_func('Smoothly interpolates between 0 and 1.\n(I think?)', 'smoothstep', names=['edge_a_', 'edge_b_', 'x_'],
        inputTypes=[['genType','float'], ['genType','float'], ['genType','genType']], 
        outputTypes=['genType','genType']),
    
    'Step' : build_func('Gives 0 where x is smaller,\n otherwise gives 1.', 'step', names=['edge_', 'x_'],
        inputTypes=[['genType','float'], ['genType','genType']], outputTypes=['genType','genType']),

    'Is Not A Number' : build_func('For each component,\nreturns true if not a number.', 'isnan', inputTypes=[['genType'], ['boolType']]),
    'Is Infinite' : build_func('For each component,\nreturns true if infinite', 'isinf', inputTypes=[['genType'], ['boolType']]),
    
# Geometric functions

    'ftransform':{
        'description' : 'Invariant vertex transformation.', 
        'inputs' : {},
        'outputs' : {'result': ['vec4']}, 
        'function' : 'result=ftransform();'
    },
    'Cross Product' : build_func('Cross product of two vectors.', 'cross', inputTypes=[['vec3'], ['vec3']], outputTypes=['vec3']),
    'Distance' : build_func('Distance between two values.', 'distance', inputTypes=[['genType'], ['genType']], outputTypes=['float']),
    'Dot Product' : build_func('Dot product of two values.', 'dot', inputTypes=[['genType'], ['genType']], outputTypes=['float']),
    'Face Forward' : build_func('Flips Direction of V\nif I and N face differently.', 'dot', names='VIN', inputTypes=[['genType'], ['genType'], ['genType']], outputTypes=['genType']),
    'Length' : build_func('Length of the vector', 'length', inputTypes=[['genType']], outputTypes=['float']),
    'Normalize' : build_func('Normalizes the vector.', 'normalize', inputTypes=[['genType']], outputTypes=['genType']),
    'Reflect' : build_func('Reflects a vector.', 'reflect', names=['in_', 'normal_'], inputTypes=[['genType'], ['genType']], outputTypes=['genType']),
    'Refract' : build_func('Refracts a vector.', 'refract', names=['in_', 'normal_', 'eta_'], inputTypes=[['genType'], ['genType'], ['float']], outputTypes=['genType']),

# Fragment processing functions (Fragment shaders only)

    'dFdx' : simple_func('Derivative in x.', 'dFdx'),
    'dFdy' : simple_func('Derivative in y.', 'dFdy'),
    'fwidth' : simple_func('Sum of the absolute derivative in x and y.', 'fwidth'),

# Matrix functions

    'Matrix Comp Multiply' : build_func('Multiplies the components\n of two matricies.', 'matrixCompMult', inputTypes=[['mat'], ['mat']], outputTypes=['mat']),
    'Outer Product Matrix' : build_func('Creates a matrix using\nthe output product of two vectors.', 'outerProduct', names='NM', 
        inputTypes=[['vec',     'vec2',     'vec2',     'vec3',     'vec3',     'vec4',     'vec4'], 
                    ['vec',     'vec3',     'vec4',     'vec2',     'vec4',     'vec2',     'vec3']], 
        outputTypes=['mat',     'mat3x2',   'mat4x2',   'mat2x3',   'mat4x3',   'mat2x4',   'mat3x4']),

    'Transpose Matrix' : build_func('Transposes a matrix.', 'transpose', names=['matrix',],
        inputTypes=[['mat', 'mat2x3', 'mat2x4', 'mat3x2', 'mat3x4', 'mat4x2', 'mat4x3']], 
        outputTypes=['mat', 'mat3x2', 'mat4x2', 'mat2x3', 'mat4x3', 'mat2x4', 'mat3x4']),
    
    'Determinant' : build_func('Gets the Deteriminant of a matrix', 'determinant', names=['matrix',], inputTypes=[['mat'],], outputTypes=['float']),
    'Inverse Matrix' : build_func('Inverses the matrix.', 'inverse', names=['matrix',], inputTypes=[['mat'],], outputTypes=['mat']),

# Vector Relational Functions

    'Boolean All' : build_func('Returns true if all values are true.', 'all', inputTypes=[['bvec']], outputTypes=['bool']),
    'Boolean Any' : build_func('Returns true if at least\none value is true.', 'any', inputTypes=[['bvec']], outputTypes=['bool']),
    'Boolean Not' : build_func('Inverts the boolean vector.', 'not', inputTypes=[['bvec']], outputTypes=['bvec']),

    'Equal' : build_func('For each component,\nreturns true if equal.', 'equal', 
        inputTypes=[['vec', 'ivec', 'bvec'], ['vec', 'ivec', 'bvec']], outputTypes=['bvec', 'bvec', 'bvec']),
    'Not Equal' : build_func('For each component,\nreturns true if not equal.', 'notEqual', 
        inputTypes=[['vec', 'ivec', 'bvec'], ['vec', 'ivec', 'bvec']], outputTypes=['bvec', 'bvec', 'bvec']),

    'Greater Than' : build_func('For each component,\nreturns true if greater than.', 'greaterThan', 
        inputTypes=[['vec', 'ivec'], ['vec', 'ivec']], outputTypes=['bvec', 'bvec']),
    'Greater Than or Equal' : build_func('For each component,\nreturns true if greater than or equal to.', 'greaterThanEqual', 
        inputTypes=[['vec', 'ivec'], ['vec', 'ivec']], outputTypes=['bvec', 'bvec']),

    'Less Than' : build_func('For each component,\nreturns true if less than.', 'lessThan', 
        inputTypes=[['vec', 'ivec'], ['vec', 'ivec']], outputTypes=['bvec', 'bvec']),
    'Less Than or Equal' : build_func('For each component,\nreturns true if less than or equal to.', 'lessThanEqual', 
        inputTypes=[['vec', 'ivec'], ['vec', 'ivec']], outputTypes=['bvec', 'bvec']),

# noise functions

    'Noise Float' : build_func('Noise value as float', 'noise1', outputTypes=['float']),
    'Noise Vec2' : build_func('Noise value as vec2', 'noise2', outputTypes=['float']),
    'Noise Vec3' : build_func('Noise value as vec3', 'noise3', outputTypes=['float']),
    'Noise Vec4' : build_func('Noise value as vec4', 'noise4', outputTypes=['float']),

}


#expands the genType for every version of the function
for inst in GLSL.values():
    c = 0
    l = list(inst['inputs'].values())
    if(len(l) > 0):
        c = l[0]
    else:
        c = list(inst['outputs'].values())[0]

    for _ in range(len(c)):

        inouts = [('inputs', k, v.pop(0)) for k,v in inst['inputs'].items()]
        inouts += [('outputs', k, v.pop(0)) for k,v in inst['outputs'].items()]

        found = ''
        for i in inouts:
            if i[2] in DataMultiTypes.keys():
                found = i[2]
                break
        
        if found != '':
            for _ in range(len(inouts)):
                orig = inouts.pop(0)
                if orig[2] == found:
                    inouts += [(orig[0], orig[1], v) for v in DataMultiTypes[found]]
                elif orig[2] in DataMultiTypes.keys() and len(DataMultiTypes[found]) == len(DataMultiTypes[orig[2]]):
                    inouts += [(orig[0], orig[1], v) for v in DataMultiTypes[orig[2]]]
                else:
                    inouts += [orig for _ in DataMultiTypes[found]]

        for v in inouts:
            inst[v[0]][v[1]].append(v[2])
    
    # remove duplicates, if input[i] == input[j]: input.pop(i), output.pop(i)
    # only checks inputs, because there shouldn't be any duplicate input data types with different outputs data types
    for i in range(len(c) - 1, 0, -1):
        keys_i = list(inst['inputs'].keys())
        
        for j in range(i - 1):
            dupe = True
            
            for k in keys_i:
                if inst['inputs'][k][i] != inst['inputs'][k][j]:
                    dupe = False
                    break
            
            if dupe:
                for k in keys_i:
                    inst['inputs'][k].pop(i)
                for k in inst['outputs'].keys():
                    inst['outputs'][k].pop(i)
    
        
'''
( example )

'Clamp' : {
    'description': 'Clamps a value or vector\nbetween a minimum and maximum.', 
    'inputs': {
        'input': ['genType','genType'],
        'min': ['genType','float'], 
        'max': ['genType','float']}, 
    'outputs': {
        'result': ['genType','genType']}, 
    'function' : 'result=clamp(input,min,max);'
}

( turns into )

'Clamp' : {
    'description': 'Clamps a value or vector\nbetween a minimum and maximum.', 
    'inputs': {
        'input' : ['float', 'vec2', 'vec3', 'vec4', 'vec2', 'vec3', 'vec4'], 
        'min': ['float', 'vec2', 'vec3', 'vec4', 'float', 'float', 'float'], 
        'max': ['float', 'vec2', 'vec3', 'vec4', 'float', 'float', 'float']}, 
    'outputs': {
        'result': ['float', 'vec2', 'vec3', 'vec4', 'vec2', 'vec3', 'vec4']}, 
    'function': 'result=clamp(input,min,max);'
}

( there ARE duplicates, don't think it matters for now )
'''
