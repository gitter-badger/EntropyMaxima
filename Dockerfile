FROM noelcjr/ccl_lectures:1.0

WORKDIR code
RUN pip install nose

ENTRYPOINT ./bin/reinstall.sh && /bin/bash