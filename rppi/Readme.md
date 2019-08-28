rppi
====

### requirements
- pacman -S --asdeps make
- pacman -S --asdeps mingw-w64-$(uname -m)-python3
- pacman -S --asdeps mingw-w64-$(uname -m)-python3-pandas
- pacman -S --asdeps mingw-w64-$(uname -m)-python3-biopython

### 构建 IRGSP(id,gene,seq)
- 从: Oryza_sativa.IRGSP-1.0.pep.all.fa
- 到: IRGSP.csv
- 处理: 
  > 去掉 description 为空和 description 中不包含 gene 信息的记录  
  > 取第一个 gene 作为参考  

### 构建 RAP_ID 和 MSU_ID 映射
- 从: RAP-MSU_2017-08-04.txt
- 到: RAP-MSU.csv
- 处理: 
  > 去掉包含 None 的行  
  > 取第二项第一个值作为参考  

### 构建 ding
- 从: Ding-378-Table_S2.xls
- 到: 
- 处理: 
  > 加载 Ding-378-Table_S2.xls  
  > 构建 ding_rap(RAP_ID_x,RAP_ID_y): 将 MSU_ID 转换成 RAP_ID  
  > 构建 ding(seq_x,seq_y): 将 RAP_ID(gene) 转换成 seq  

### 构建 prin
- 从: PRIN_V1.0_rice_experimental_determined_interactions.xls
- 到: 
- 处理: 
  > 加载 PRIN_V1.0_rice_experimental_determined_interactions.xls  
  > 构建 prin_rap(RAP_ID_x,RAP_ID_y): 将 MSU_ID 转换成 RAP_ID  
  > 构建 prin(seq_x,seq_y): 将 RAP_ID(gene) 转换成 seq  

### 构建 Subcellular-localization-RAP.csv
- 从: 
- 到: Subcellular-localization-RAP.csv
- 处理: 
  > 从 uniprot 下载 *.fasta.gz  
  > 使用 make uniprot-ids 导出 id 文件  
  > 将 id 文件 上传到 uniprot, 下载 tab 文件  
  > 提取 tab 文件中的 rap_id  
  > 使用全局笛卡尔积减去局部笛卡尔积的方法计算(rap_id_x,rap_id_y)  

### 构建 uniprot
- 从: Subcellular-localization-RAP.csv
- 到: 
- 处理: 
  > 加载 Subcellular-localization-RAP.csv  
  > 构建 prin(seq_x,seq_y): 将 RAP_ID(gene) 转换成 seq  
