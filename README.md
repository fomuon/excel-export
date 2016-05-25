# excel-export
포멧 정보가 포함된 엑셀 파일로부터 table 별로 분리된 정보를 sqlite db 와 sql text 파일로 추출한다.

## Installation

```
$pip install excel-export
```
or
```
$pip install git+https://github.com/fomuon/excel-export.git
```

## Command-Line 사용법

sample_excel.xlsx에 정의된 sample_table, sample_table2, sample_table3 테이블에 대해 sqlite3 db 파일과 sql text 파일을 출력한다.
```
$ excel-export -I sample_excel.xlsx
```

## 워크시트내 작성 규칙

* 1행에 반드시 테이블명을 다음 패턴으로 작성하고 그 아래 작성되는 컬럼정보의 열에 맞게 셀병합 한다.
	* EXP:$table_name:$설명
* 2행에는 컬럼 정보 작성 또는 컬럼 설명을 작성한다. 컬럼 설명을 작성하였다면 3행에 컬럼 정보를 작성한다.
	* $column_name:@TYPE
	* @TYPE : I - Integer, T - Text, N - Numeric
* 3행 또는 4행부터는 데이터행이며 셀병합된 열의 값은 모두 같은 값으로 처리된다.