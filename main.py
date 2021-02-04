import translator as c
import driver as d
import codegen as cg

# get code generator
code_gen: cg.ICodeGen = cg.CLangCodeGen()
# get translator
converter: c.ITranslator = c.ILTranslator()
# driver instance
driver: d.IDriver = d.DriverImpl(converter, code_gen)

try:
    code = driver.translate('test.py')
    print(code)
    #with open("out.c", "w") as f:
    #    f.write(code)
except Exception as ex:
    raise ex
    # print(ex)
