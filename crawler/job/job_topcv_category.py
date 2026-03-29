import sys
import os
# Thêm dòng này để Python tìm thấy thư mục 'engine' ở thư mục cha
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Bây giờ mới import crawler
from engine import crawler
    
    
print(crawler.run_category('metadata//topcv_category.json'))

