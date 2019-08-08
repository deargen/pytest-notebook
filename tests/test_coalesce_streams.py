import os

import nbformat

from pytest_notebook.post_processors import coalesce_streams
from pytest_notebook.utils import prepare_cell_v4


path = os.path.dirname(os.path.realpath(__file__))


def test_coalesce_streams_same():
    """Test coalesce_streams if no streams require merging."""
    notebook = nbformat.read(
        os.path.join(path, "raw_files", "different_outputs.ipynb"), as_version=4
    )
    new_notebook = coalesce_streams(notebook)
    assert notebook == new_notebook


def test_coalesce_streams():
    """Test coalesce_streams if streams require merging."""
    notebook = nbformat.v4.new_notebook()
    notebook.cells.append(
        prepare_cell_v4(
            {
                "cell_type": "code",
                "execution_count": 3,
                "metadata": {},
                "outputs": [
                    {"name": "stdout", "output_type": "stream", "text": ["hallo1\n"]},
                    {"name": "stdout", "output_type": "stream", "text": ["hallo2\n"]},
                ],
                "source": "".join(["print('hallo1')\n", "print('hallo2')"]),
            }
        )
    )
    expected = nbformat.v4.new_notebook()
    expected.cells.append(
        prepare_cell_v4(
            {
                "cell_type": "code",
                "execution_count": 3,
                "metadata": {},
                "outputs": [
                    {
                        "name": "stdout",
                        "output_type": "stream",
                        "text": ["hallo1\nhallo2\n"],
                    }
                ],
                "source": "".join(["print('hallo1')\n", "print('hallo2')"]),
            }
        )
    )
    new_notebook = coalesce_streams(notebook)
    assert new_notebook == expected
