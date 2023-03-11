FROM public.ecr.aws/lambda/python:3.8


COPY api ./api
COPY datasets ./datasets
COPY models ./models

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY main.py ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]