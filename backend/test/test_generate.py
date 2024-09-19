import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
from helper.llm import Gemini, GPT
from typing import List
from schemas.message import MessageResponse

def generate_message(
    instruction: str,
    chats: List[str],
    context: str,
    question: str,
    config_llm: dict
):
    llm_name = config_llm['llm_name']
        
    if llm_name[:3] == 'gpt':
        model = GPT(model_name=config_llm['llm_name'],
                    temperature=config_llm['temperature'],
                    top_p=config_llm['top_p'],
                    frequency_penalty=config_llm['frequency_penalty'],
                    presence_penalty=config_llm['presence_penalty'],
                    max_length=config_llm['max_length'],
                    output_format=config_llm['output_format'])
        
        messages = model.get_messages(instruction, question, chats, context)
        response = model.invoke(messages)

        return MessageResponse(
            answer=response.choices[0].message.content,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens
        )

    else:
        model = Gemini(model_name=config_llm['llm_name'],
                       temperature=config_llm['temperature'],
                       top_p=config_llm['top_p'],
                       max_length=config_llm['max_length'])
        
        messages = model.get_messages(instruction, question, chats, context)
        response = model.invoke(messages)

        return MessageResponse(
            answer=response.text,
            input_tokens=response.usage_metadata.prompt_token_count,
            output_tokens=response.usage_metadata.candidates_token_count
        )

instruction = '''# Character
Bạn là một chuyên gia marketing hiểu biết sâu rộng về các chiến lược và công cụ tiếp thị hiện đại. Bạn có khả năng phát triển và tối ưu hóa chiến dịch tiếp thị hiệu quả dựa trên yêu cầu của khách hàng.

## Skills
### Skill 1: Phân tích thị trường
- Khám phá và phân tích xu hướng thị trường hiện tại.
- Sử dụng googleWebSearch() để tìm kiếm thông tin và thống kê mới nhất liên quan đến dịch vụ hoặc sản phẩm của khách hàng.
- Tóm tắt những điểm quan trọng và gợi ý chiến lược marketing dựa trên phân tích.

### Skill 2: Phát triển chiến dịch tiếp thị
- Xây dựng kế hoạch tiếp thị chi tiết dựa trên yêu cầu của khách hàng.
- Sử dụng công cụ quảng cáo trên các nền tảng như Google AdWords, Facebook, Instagram để tiếp cận đối tượng mục tiêu.
- Đề xuất các kênh tiếp thị phù hợp và cách tối ưu hóa hiệu quả chiến dịch.

### Skill 3: Đo lường và tối ưu hóa
- Sử dụng các công cụ như Google Analytics, Facebook Insights để theo dõi và đo lường hiệu quả chiến dịch.
- Đánh giá kết quả và đề xuất cách cải thiện nếu cần thiết.
- Báo cáo kết quả chi tiết theo yêu cầu của khách hàng.

## Constraints
- Chỉ thảo luận về các chủ đề liên quan đến marketing.
- Chỉ sử dụng những nguồn tin cậy trong việc cung cấp thông tin.
- Sử dụng kết hợp các kiến thức nội bộ và công cụ tìm kiếm để có thông tin chính xác và cập nhật.
'''

context = '''Tóm tắt thông số cấu hình Galaxy A55 5G:

Màn hình: Kích thước 6.6 inch, tấm nền AMOLED, độ phân giải Full HD+ (1.080 x 2.340 pixels), tần số quét 120 Hz.
CPU: Exynos 1480.
RAM: 8 GB hoặc 12 GB.
Bộ nhớ trong: 128 GB hoặc 256 GB (hỗ trợ mở rộng tối đa 1 TB qua thẻ microSD).
Camera sau: 50 MP (chính) + 12 MP (góc siêu rộng) + 5 MP (macro).
Camera trước: 32 MP.
Dung lượng pin: 5.000 mAh, hỗ trợ sạc nhanh 25 W.
Hệ điều hành: One UI 6.1 - Android 14.'''

question = 'Hãy viết một bài marketing cho chiếc điện thoại Galaxy A55 5G.'


# model = GPT(model_name='gpt-3.5-turbo-0125',
#             temperature=0.7,
#             top_p=0.5,
#             frequency_penalty=0,
#             presence_penalty=0,
#             max_length=1024,
#             output_format='json_object')

config_llm = {
    'llm_name': 'gpt-4o-mini',
    'temperature': 0.7,
    'top_p': 0.5,
    'frequency_penalty': 0,
    'presence_penalty': 0,
    'max_length': 1024,
    'output_format': 'text'
}

print(generate_message(instruction, [], context, question, config_llm))