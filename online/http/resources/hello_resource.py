from flask_restful import Resource

class HelloResource(Resource):
    """
    hello路由
    快速检查服务是否健康
    """

    def get(self):
        return 'hello'
