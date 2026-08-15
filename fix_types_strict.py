import re

types_path = "frontend/src/types/index.ts"
with open(types_path, "r") as f:
    code = f.read()

# Remove optionals that are strictly used
code = code.replace("severity?: string;", "severity: string;")
code = code.replace("type?: string;", "type: string;")
code = code.replace("location?: string;", "location: string;")
code = code.replace("descriptionKey?: string;", "descriptionKey: string;")
code = code.replace("available?: number | string;", "available: number | string;")
code = code.replace("total?: number | string;", "total: number | string;")
code = code.replace("id?: string | number;", "id: string | number;")
code = code.replace("id?: string;", "id: string;")
code = code.replace("icon?: string;", "icon: string;")
code = code.replace("titleKey?: string;", "titleKey: string;")
code = code.replace("resource?: string;", "resource: string;")
code = code.replace("name?: string;", "name: string;")
code = code.replace("to?: string;", "to: string;")
code = code.replace("from?: string;", "from: string;")
code = code.replace("eta?: string;", "eta: string;")

with open(types_path, "w") as f:
    f.write(code)

