from google.appengine.api import taskqueue

q = taskqueue.Queue('pull-queue')
tasks = []
payload_str = 'hello world'
tasks.append(taskqueue.Task(payload=payload_str, method='PULL'))
q.add(tasks)
