var tests={"section-eof": {"test": "![", "doc": "{["}, "sq-eof": {"test": "!'", "doc": "{'"}, "escapes": {"test": "(3\"8:\\[\\]{\\}~A.\"{6\"7:escapes\"\"10:\\{:}[]\"'` \"\"5:\"\\'\\`\"\"5:\\\"'\\`\"\"5:\\\"\\'`\"[1\"6:\\[]{\\}\"]2\"6:quoted\"\"21:\\a\\b\\t\\f\\v\\uabcde\\xab\"\"12:unrecognized\"\"21:\\a\\b\\t\\f\\v\\uabcde\\xab\"}\"2:~A.\\\")", "doc": "\\[\\]\\{\\}\r\n{escapes \\\\\\{\\:\\}\\[\\]\\\"\\'\\`\\  \"\\\"\\'\\`\" '\\\"\\'\\`' `\\\"\\'\\`` [\\[\\]\\{\\}] unrecognized:\\a\\b\\t\\f\\v\\uabcde\\xab quoted:\"\\a\\b\\t\\f\\v\\uabcde\\xab\"}\r\n\\"}, "bq-eof": {"test": "!`", "doc": "{`"}, "nontextual-name": {"test": "(8{1{1[1\"3:tag\"]0}0}\"1:~A.\"{1[2\"7:section\"{1\"3:tag\"0}]0}\"1:~A.\"{1\"3:tag\"1{1\"4:attr\"0}\"5:value\"}\"1:~A.\"{1\"3:tag\"1[1\"4:attr\"]\"5:value\"}\"1:~A.\")", "doc": "{{[tag]}}\r\n{[section{tag}]}\r\n{tag {attr}:value}\r\n{tag [attr]:value}\r\n"}, "control-chars": {"test": "(3\"43:This file contains many control characters~A.\"{2\"3:tag\"\"33:~.~1.~2.~3.~4.~5.~6.~7.~8.~9.~A.~A.~A.~A.~E.~F.~10.~11.~12.~13.~14.~15.~16.~17.~18.~19.~1A.~1B.~1C.~1D.~1E.~1F.~7F.\"0}\"1:~A.\")", "doc": "This file contains many control characters\r\n{tag \u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\b\\\t\\\n\\\u000b\\\f\\\r\u000e\u000f\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019\u001a\u001b\u001c\u001d\u001e\u001f\u007f}\r\n"}, "newline": {"test": "(1\"55:Line 1~A.Line 2~A.Line 3~A.Line 4~A.Line 5~A.Line 6~A.Line 7~A.Line 8\")", "doc": "Line 1\r\nLine 2\nLine 3\fLine 4\rLine 5\u0085Line 6\u2028Line 7\u2029Line 8"}, "duplicate-attribute": {"test": "!::", "doc": "{a:b a:c}"}, "valueless-attribute": {"test": "!:?", "doc": "{v:}"}, "tag-eof": {"test": "!{", "doc": "{"}, "unicode": {"test": "(1{1\"3:~30C7.~30FC.~30BF.\"2\"7:alchemy\"\"2:~1F700.~7E.\"\"2:~5C5E.~6027.\"\"1:~5024.\"})", "doc": "{\u30c7\u30fc\u30bf \u5c5e\u6027:\u5024 alchemy:\ud83d\udf00~}"}, "basic": {"test": "(3{5\"5:root1\"\"3:pos\"\"3:pos\"\"3:pos\"\"3:pos\"1\"4:name\"\"4:attr\"}\"1:~A.\"{2\"5:root2\"[2\"8:section \"{1\"3:tag\"0}]1\"4:name\"[2\"8:section \"{1\"3:tag\"0}]})", "doc": "{root1 \"pos\" 'pos' `pos` pos name:attr}\n{root2 [section {tag}] name:[section {tag}]}"}, "unescaped-brace": {"test": "!{]", "doc": "{[{]}"}, "unexpected-colon": {"test": "!:", "doc": "{:x}"}, "dq-eof": {"test": "!\"", "doc": "{\""}}