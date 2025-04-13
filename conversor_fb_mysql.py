import fdb

# 🔧 CONFIGURAÇÕES DO FIREBIRD
FIREBIRD_HOST = 'localhost'
FIREBIRD_PATH = 'C:/WN/Gestao/Dados/DADOS.fdb'
FIREBIRD_USER = 'SYSDBA'
FIREBIRD_PASSWORD = 'masterkey'

# 📄 Nome do arquivo de saída
output_file = 'estrutura_mysql.sql'

# Conectar ao Firebird
conn = fdb.connect(
    host=FIREBIRD_HOST,
    database=FIREBIRD_PATH,
    user=FIREBIRD_USER,
    password=FIREBIRD_PASSWORD
)

cur = conn.cursor()

# Obter todas as tabelas de usuário
cur.execute("""
    SELECT TRIM(rdb$relation_name)
    FROM rdb$relations
    WHERE rdb$system_flag = 0 AND rdb$view_blr IS NULL
""")
tables = [row[0] for row in cur.fetchall()]

def map_type(fb_type, fb_length, fb_subtype):
    type_map = {
        7: 'SMALLINT',
        8: 'INTEGER',
        10: 'FLOAT',
        12: 'DATE',
        13: 'TIME',
        14: f'CHAR({fb_length})',
        16: 'BIGINT',
        27: 'DOUBLE',
        35: 'DATETIME',
        37: f'VARCHAR({fb_length})',
        261: 'TEXT' if fb_subtype == 1 else 'BLOB',
    }

    # Se for o tipo UNKNOWN_TYPE (23), converta para BOOLEAN
    if fb_type == 23:
        return 'BOOLEAN'
    
    # Se for o tipo UNKNOWN_TYPE (26), converta para BLOB
    if fb_type == 26:
        return 'BLOB'

    return type_map.get(fb_type, f'UNKNOWN_TYPE({fb_type})')

# Abre o arquivo para escrita
with open(output_file, 'w', encoding='utf-8') as f:
    for table in tables:
        f.write(f"\n-- Tabela: {table}\n")
        f.write(f"CREATE TABLE `{table}` (\n")

        cur.execute(f"""
            SELECT
                TRIM(rf.rdb$field_name),
                f.rdb$field_type,
                f.rdb$field_length,
                f.rdb$field_sub_type,
                f.rdb$null_flag
            FROM rdb$relation_fields rf
            JOIN rdb$fields f ON rf.rdb$field_source = f.rdb$field_name
            WHERE rf.rdb$relation_name = '{table}'
            ORDER BY rf.rdb$field_position
        """)

        cols = []
        for row in cur.fetchall():
            name, fb_type, length, subtype, null_flag = row
            mysql_type = map_type(fb_type, length, subtype)
            null_str = 'NOT NULL' if null_flag == 1 else 'NULL'
            cols.append(f"  `{name}` {mysql_type} {null_str}")

        f.write(",\n".join(cols))
        f.write("\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n")

print(f"✅ Estrutura exportada para o arquivo: {output_file}")